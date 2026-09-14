from typing import Any


def normalize_text(value: Any) -> str:
    if value is None:
        return ""

    return str(value).strip().lower()


def detect_red_flags(
    complaint: str,
    answers: dict[str, Any],
) -> dict[str, Any]:

    complaint_text = normalize_text(complaint)

    all_text = " ".join(
        [
            complaint_text,
            *[
                normalize_text(value)
                for value in answers.values()
            ],
        ]
    )

    flags = []

    # -------------------------------------------------
    # CHEST PAIN RED FLAGS
    # -------------------------------------------------

    chest_pain_terms = [
        "chest pain",
        "pain in chest",
        "chest discomfort",
        "pressure in chest",
        "tightness in chest",
    ]

    breathing_terms = [
        "difficulty breathing",
        "breathing difficulty",
        "shortness of breath",
        "breathlessness",
        "can't breathe",
        "cannot breathe",
    ]

    sweating_terms = [
        "sweating",
        "sweating heavily",
        "cold sweat",
    ]

    fainting_terms = [
        "fainted",
        "fainting",
        "passed out",
        "unconscious",
    ]

    chest_pain = any(
        term in all_text
        for term in chest_pain_terms
    )

    breathing_difficulty = any(
        term in all_text
        for term in breathing_terms
    )

    sweating = any(
        term in all_text
        for term in sweating_terms
    )

    fainting = any(
        term in all_text
        for term in fainting_terms
    )

    if chest_pain and (
        breathing_difficulty
        or sweating
        or fainting
    ):
        flags.append(
            {
                "type": "chest_pain",
                "severity": "urgent",
                "message": (
                    "Chest pain with additional concerning "
                    "symptoms was reported."
                ),
            }
        )

    # -------------------------------------------------
    # SEVERE BREATHING DIFFICULTY
    # -------------------------------------------------

    severe_breathing_terms = [
        "cannot breathe",
        "can't breathe",
        "unable to breathe",
        "very difficult to breathe",
        "severe breathing difficulty",
    ]

    if any(
        term in all_text
        for term in severe_breathing_terms
    ):
        flags.append(
            {
                "type": "breathing",
                "severity": "urgent",
                "message": (
                    "Severe breathing difficulty was reported."
                ),
            }
        )

    # -------------------------------------------------
    # FAINTING / LOSS OF CONSCIOUSNESS
    # -------------------------------------------------

    if fainting:
        flags.append(
            {
                "type": "fainting",
                "severity": "urgent",
                "message": (
                    "Fainting or loss of consciousness "
                    "was reported."
                ),
            }
        )

    # -------------------------------------------------
    # SEVERE HEADACHE + NEUROLOGICAL SYMPTOMS
    # -------------------------------------------------

    headache_terms = [
        "severe headache",
        "worst headache",
        "very severe headache",
        "sudden severe headache",
    ]

    neurological_terms = [
        "weakness",
        "numbness",
        "confusion",
        "difficulty speaking",
        "slurred speech",
        "vision loss",
        "blurred vision",
        "seizure",
        "convulsion",
    ]

    severe_headache = any(
        term in all_text
        for term in headache_terms
    )

    neurological_symptom = any(
        term in all_text
        for term in neurological_terms
    )

    if severe_headache and neurological_symptom:
        flags.append(
            {
                "type": "neurological",
                "severity": "urgent",
                "message": (
                    "Severe headache with a neurological "
                    "symptom was reported."
                ),
            }
        )

    # -------------------------------------------------
    # GENERAL SEVERE SYMPTOMS
    # -------------------------------------------------

    emergency_terms = [
        "severe bleeding",
        "heavy bleeding",
        "vomiting blood",
        "blood in vomit",
        "black stool",
        "seizure",
        "unconscious",
        "unresponsive",
    ]

    if any(
        term in all_text
        for term in emergency_terms
    ):
        flags.append(
            {
                "type": "general",
                "severity": "urgent",
                "message": (
                    "A potentially serious symptom "
                    "was reported."
                ),
            }
        )

    # -------------------------------------------------
    # EXTREMELY HIGH FEVER / TEMPERATURE
    # -------------------------------------------------

    temperature_celsius = None

    # The fever interview pathway stores the patient's
    # highest measured temperature in the "severity"
    # field.
    #
    # Example:
    #
    # answers = {
    #     "onset": "...",
    #     "duration": "...",
    #     "severity": 41
    # }
    #
    # IMPORTANT:
    # "severity" is only treated as temperature when
    # the chief complaint is actually fever.
    #
    # This prevents a headache severity of 10 or another
    # symptom severity score from being interpreted as
    # 10°C.

    temperature_keys = [
        "temperature",
        "temp",
        "body_temperature",
        "temperature_celsius",
        "temperature_c",
    ]

    # First check for a dedicated temperature field.
    for key in temperature_keys:

        if key in answers:

            try:
                value = answers[key]

                if value is None or str(value).strip() == "":
                    continue

                temperature_celsius = float(value)

                break

            except (TypeError, ValueError):
                continue

    # Fever complaint indicators.
    fever_indicators = [
        "fever",
        "high temperature",
        "बुखार",
        "ताप",
        "ताप आला",
        "জ্বর",
        "காய்ச்சல்",
        "జ్వరం",
    ]

    is_fever_complaint = any(
        indicator in complaint_text
        for indicator in fever_indicators
    )

    # In the actual MediKiosk fever pathway, the
    # temperature question uses field="severity".
    #
    # Only use it when this is a fever complaint.
    if (
        temperature_celsius is None
        and is_fever_complaint
        and "severity" in answers
    ):

        try:
            value = answers["severity"]

            if value is not None and str(value).strip() != "":
                temperature_celsius = float(value)

        except (TypeError, ValueError):
            pass

    # -------------------------------------------------
    # LIFE-THREATENING FEVER THRESHOLD
    # -------------------------------------------------

    # Temperature strictly ABOVE 40°C is classified
    # as life-threatening.
    #
    # 40.0°C  -> not triggered by this rule
    # 40.1°C  -> life-threatening
    # 41.0°C  -> life-threatening
    # 50.0°C  -> life-threatening

    if (
        temperature_celsius is not None
        and temperature_celsius > 40.0
    ):
        flags.append(
            {
                "type": "extreme_fever",
                "severity": "life_threatening",
                "message": (
                    f"Extremely high body temperature "
                    f"({temperature_celsius:.1f}°C) was reported."
                ),
            }
        )

    # -------------------------------------------------
    # FINAL RESULT
    # -------------------------------------------------

    if flags:

        # If ANY red flag is life-threatening,
        # the overall assessment must be
        # life-threatening.

        has_life_threatening = any(
            flag.get("severity") == "life_threatening"
            for flag in flags
        )

        if has_life_threatening:

            urgency = "life_threatening"

            message = (
                "A potentially life-threatening warning "
                "sign was detected. Please alert a "
                "healthcare professional immediately."
            )

        else:

            urgency = "urgent"

            message = (
                "Please alert a healthcare professional "
                "immediately. Some of your responses may "
                "require urgent clinical attention."
            )

        return {
            "has_red_flags": True,
            "urgency": urgency,
            "message": message,
            "flags": flags,
        }

    # -------------------------------------------------
    # NO RED FLAGS
    # -------------------------------------------------

    return {
        "has_red_flags": False,
        "urgency": "routine",
        "message": (
            "No predefined urgent warning pattern "
            "was detected."
        ),
        "flags": [],
    }