const visit = { patientId: "", language: "English", concern: "", documents: [] };
let recognition;

function goToScreen(id) { document.querySelectorAll(".screen").forEach(s => s.classList.remove("active")); document.getElementById(id).classList.add("active"); window.scrollTo(0, 0); }
function startIntake() { const id = document.getElementById("patient-id").value.trim(), error = document.getElementById("identity-error"); if (!id) { error.textContent = "Please enter your ABHA number or mobile number."; return; } visit.patientId = id; error.textContent = ""; goToScreen("consent-screen"); }
function startGuestIntake() { visit.patientId = "New patient"; goToScreen("consent-screen"); }
function acceptConsent() { const approved = ["consent-history","consent-documents","consent-share"].every(id => document.getElementById(id).checked), error = document.getElementById("consent-error"); if (!approved) { error.textContent = "Please confirm each consent item before continuing."; return; } error.textContent = ""; goToScreen("intake-screen"); }
function continueIntake() { const concern = document.getElementById("concern-input").value.trim(), error = document.getElementById("intake-error"), urgent = /chest pain|difficulty breathing|cannot breathe|stroke|unconscious|severe bleeding|suicid/i.test(concern); if (!concern) { error.textContent = "Please describe your main health concern."; return; } if (urgent) { document.getElementById("red-flag-alert").hidden = false; error.textContent = "Please alert a staff member before continuing."; return; } visit.concern = concern; error.textContent = ""; goToScreen("documents-screen"); }
function showDocuments() { visit.documents = [...document.getElementById("medical-documents").files]; document.getElementById("document-list").innerHTML = visit.documents.map(f => "<li>✓ " + escapeHtml(f.name) + "</li>").join(""); }
function createSummary() { document.getElementById("summary-patient").textContent = visit.patientId; document.getElementById("summary-language").textContent = visit.language; document.getElementById("summary-concern").textContent = visit.concern; document.getElementById("summary-documents").textContent = visit.documents.length ? visit.documents.length + " document(s) selected" : "None"; goToScreen("summary-screen"); }
function submitSummary() { goToScreen("complete-screen"); }
function cycleLanguage() { visit.language = visit.language === "English" ? "हिन्दी" : "English"; document.getElementById("language-switch").textContent = visit.language; }
function toggleAccessibility() { document.body.classList.toggle("accessible"); }
function toggleVoiceCapture() {
 const status=document.getElementById("voice-status"), button=document.getElementById("voice-button"), API=window.SpeechRecognition||window.webkitSpeechRecognition;
 if (!API) { status.textContent="Voice input is not available in this browser. Please type your concern."; return; }
 if (recognition) { recognition.stop(); return; }
 recognition=new API(); recognition.lang=visit.language === "हिन्दी" ? "hi-IN" : "en-IN";
 recognition.onstart=()=>{status.textContent="Listening… speak naturally.";button.classList.add("recording");};
 recognition.onresult=e=>{const input=document.getElementById("concern-input");input.value+=(input.value ? " " : "")+e.results[0][0].transcript;};
 recognition.onerror=()=>{status.textContent="We could not hear that. You can try again or type your concern.";};
 recognition.onend=()=>{recognition=null;button.classList.remove("recording");if(!status.textContent.includes("could not"))status.textContent="Voice note added. You may continue speaking or edit the text.";};
 recognition.start();
}
function newVisit() { location.reload(); }
function escapeHtml(value) { const div=document.createElement("div"); div.textContent=value; return div.innerHTML; }
const visit = {
  patientId: "",
  language: "English",
  concern: "",
  documents: []
};

let recognition;

function goToScreen(id) {
  document.querySelectorAll(".screen").forEach(screen => {
    screen.classList.remove("active");
  });

  document.getElementById(id).classList.add("active");
  window.scrollTo(0, 0);
}

function startIntake() {
  const patientId = document.getElementById("patient-id").value.trim();
  const error = document.getElementById("identity-error");

  if (!patientId) {
    error.textContent = "Please enter your ABHA number or mobile number.";
    return;
  }

  visit.patientId = patientId;
  error.textContent = "";
  goToScreen("consent-screen");
}

function startGuestIntake() {
  visit.patientId = "New patient";
  goToScreen("consent-screen");
}

function acceptConsent() {
  const approved = [
    "consent-history",
    "consent-documents",
    "consent-share"
  ].every(id => document.getElementById(id).checked);

  const error = document.getElementById("consent-error");

  if (!approved) {
    error.textContent = "Please confirm each consent item before continuing.";
    return;
  }

  error.textContent = "";
  goToScreen("intake-screen");
}

function continueIntake() {
  const concern = document.getElementById("concern-input").value.trim();
  const error = document.getElementById("intake-error");

  const urgentSymptoms =
    /chest pain|difficulty breathing|cannot breathe|stroke|unconscious|severe bleeding|suicid/i;

  if (!concern) {
    error.textContent = "Please describe your main health concern.";
    return;
  }

  if (urgentSymptoms.test(concern)) {
    document.getElementById("red-flag-alert").hidden = false;
    error.textContent = "Please alert a staff member before continuing.";
    return;
  }

  visit.concern = concern;
  error.textContent = "";
  goToScreen("documents-screen");
}

function showDocuments() {
  visit.documents = [
    ...document.getElementById("medical-documents").files
  ];

  document.getElementById("document-list").innerHTML =
    visit.documents
      .map(file => `<li>✓ ${escapeHtml(file.name)}</li>`)
      .join("");
}

function createSummary() {
  document.getElementById("summary-patient").textContent = visit.patientId;
  document.getElementById("summary-language").textContent = visit.language;
  document.getElementById("summary-concern").textContent = visit.concern;

  document.getElementById("summary-documents").textContent =
    visit.documents.length
      ? `${visit.documents.length} document(s) selected`
      : "None";

  goToScreen("summary-screen");
}

function submitSummary() {
  goToScreen("complete-screen");
}

function cycleLanguage() {
  visit.language = visit.language === "English" ? "हिन्दी" : "English";
  document.getElementById("language-switch").textContent = visit.language;
}

function toggleAccessibility() {
  document.body.classList.toggle("accessible");
}

function toggleVoiceCapture() {
  const status = document.getElementById("voice-status");
  const button = document.getElementById("voice-button");
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    status.textContent =
      "Voice input is not available in this browser. Please type your concern.";
    return;
  }

  if (recognition) {
    recognition.stop();
    return;
  }

  recognition = new SpeechRecognition();
  recognition.lang = visit.language === "हिन्दी" ? "hi-IN" : "en-IN";

  recognition.onstart = () => {
    status.textContent = "Listening… speak naturally.";
    button.classList.add("recording");
  };

  recognition.onresult = event => {
    const input = document.getElementById("concern-input");

    input.value +=
      `${input.value ? " " : ""}${event.results[0][0].transcript}`;
  };

  recognition.onerror = () => {
    status.textContent =
      "We could not hear that. You can try again or type your concern.";
  };

  recognition.onend = () => {
    recognition = null;
    button.classList.remove("recording");
  };

  recognition.start();
}

function newVisit() {
  location.reload();
}

function escapeHtml(value) {
  const div = document.createElement("div");
  div.textContent = value;
  return div.innerHTML;
}