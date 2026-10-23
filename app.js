const form = document.getElementById("student-form");
const submitButton = form.querySelector("button[type=submit]");
const buttonLabel = submitButton.querySelector(".button-label");
const errorBox = document.getElementById("form-error");
const emptyState = document.getElementById("empty-state");
const resultState = document.getElementById("result-state");

async function checkService() {
  const dot = document.getElementById("status-dot");
  const text = document.getElementById("status-text");
  try {
    const response = await fetch("/health");
    const data = await response.json();
    if (!response.ok || !data.model_loaded) throw new Error("Model unavailable");
    dot.classList.add("online");
    text.textContent = "Model ready";
  } catch {
    dot.classList.add("offline");
    text.textContent = "Service unavailable";
  }
}

function showProbabilities(probabilities) {
  const target = document.getElementById("probabilities");
  const order = ["Beneficial", "Neutral", "Negative"];
  target.innerHTML = "";
  order.forEach((label) => {
    const value = Number(probabilities[label] || 0);
    const row = document.createElement("div");
    row.className = "prob-row";
    const name = document.createElement("div");
    name.className = "prob-label";
    const strong = document.createElement("strong");
    strong.textContent = label;
    const percent = document.createElement("span");
    percent.textContent = (value * 100).toFixed(1) + "%";
    name.append(strong, percent);
    const track = document.createElement("div");
    track.className = "prob-track";
    const bar = document.createElement("span");
    bar.style.width = Math.max(0, Math.min(100, value * 100)) + "%";
    track.appendChild(bar);
    row.append(name, track);
    target.appendChild(row);
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorBox.hidden = true;
  submitButton.disabled = true;
  buttonLabel.textContent = "Calculating…";

  const values = new FormData(form);
  const payload = {
    Age: Number(values.get("Age")),
    Gender: values.get("Gender"),
    Academic_Level: values.get("Academic_Level"),
    Primary_Platform: values.get("Primary_Platform"),
    Daily_Usage_Hours: Number(values.get("Daily_Usage_Hours")),
    Weekend_Extra_Hours: Number(values.get("Weekend_Extra_Hours")),
    Device_Type: values.get("Device_Type"),
    Sleep_Duration_Hours: Number(values.get("Sleep_Duration_Hours")),
    Sleep_Quality_Score: Number(values.get("Sleep_Quality_Score")),
    Late_Night_Usage: form.elements.Late_Night_Usage.checked,
    Social_Comparison_Frequency: values.get("Social_Comparison_Frequency"),
  };

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: {"Content-Type": "application/json", "Accept": "application/json"},
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) {
      const detail = Array.isArray(data.detail) ? data.detail.map((item) => item.msg).join("; ") : "The model could not process these values.";
      throw new Error(detail);
    }
    document.getElementById("impact-value").textContent = data.overall_impact;
    const impact = document.getElementById("impact-value");
    impact.classList.remove("is-neutral", "is-negative");
    if (data.overall_impact === "Neutral") impact.classList.add("is-neutral");
    if (data.overall_impact === "Negative") impact.classList.add("is-negative");
    const score = Math.max(0, Math.min(100, Number(data.mental_health_index)));
    document.getElementById("mental-score").textContent = score.toFixed(1);
    document.getElementById("score-fill").style.width = score + "%";
    showProbabilities(data.overall_impact_probabilities || {});
    emptyState.hidden = true;
    resultState.hidden = false;
    resultState.scrollIntoView({behavior: "smooth", block: "nearest"});
  } catch (error) {
    errorBox.textContent = error.message || "Unable to reach the model. Please try again.";
    errorBox.hidden = false;
  } finally {
    submitButton.disabled = false;
    buttonLabel.textContent = "Explore estimate";
  }
});

checkService();
