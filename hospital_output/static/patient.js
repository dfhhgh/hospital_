const appointmentForm = document.getElementById("appointmentForm");
const appointmentList = document.getElementById("appointmentList");
const clearAppointmentsBtn = document.getElementById("clearAppointmentsBtn");

const moodForm = document.getElementById("moodForm");
const moodButtons = document.querySelectorAll(".mood-btn");
const painLevel = document.getElementById("painLevel");
const energyLevel = document.getElementById("energyLevel");
const painValue = document.getElementById("painValue");
const energyValue = document.getElementById("energyValue");
const moodHistoryBody = document.getElementById("moodHistoryBody");
const clearMoodBtn = document.getElementById("clearMoodBtn");

const snapshotMood = document.getElementById("snapshotMood");
const snapshotPain = document.getElementById("snapshotPain");
const snapshotEnergy = document.getElementById("snapshotEnergy");
const snapshotNote = document.getElementById("snapshotNote");

let selectedMood = "";

function setEmptyAppointments() {
  appointmentList.innerHTML = "";
  const empty = document.createElement("p");
  empty.className = "empty-state";
  empty.textContent = "No appointments booked yet.";
  appointmentList.appendChild(empty);
}

function setEmptyMoodHistory() {
  moodHistoryBody.innerHTML = `
    <tr class="empty-row">
      <td colspan="5">No health mood entries yet.</td>
    </tr>
  `;
}

function formatDateTime(date, time) {
  return `${date} at ${time}`;
}

function createAppointmentCard({
  department,
  doctor,
  appointmentDate,
  appointmentTime,
  reason,
}) {
  const card = document.createElement("article");
  card.className = "appointment-item";

  const title = document.createElement("h3");
  title.textContent = `${department} - ${doctor}`;

  const meta = document.createElement("p");
  meta.className = "appointment-meta";
  meta.textContent = formatDateTime(appointmentDate, appointmentTime);

  const reasonText = document.createElement("p");
  reasonText.className = "appointment-reason";
  reasonText.textContent = reason;

  card.appendChild(title);
  card.appendChild(meta);
  card.appendChild(reasonText);
  return card;
}

function clearAppointmentEmptyState() {
  const emptyState = appointmentList.querySelector(".empty-state");
  if (emptyState) {
    emptyState.remove();
  }
}

appointmentForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const department = document.getElementById("department").value;
  const doctor = document.getElementById("doctor").value.trim();
  const appointmentDate = document.getElementById("appointmentDate").value;
  const appointmentTime = document.getElementById("appointmentTime").value;
  const reason = document.getElementById("reason").value.trim();

  if (
    !department ||
    !doctor ||
    !appointmentDate ||
    !appointmentTime ||
    !reason
  ) {
    return;
  }

  clearAppointmentEmptyState();
  appointmentList.appendChild(
    createAppointmentCard({
      department,
      doctor,
      appointmentDate,
      appointmentTime,
      reason,
    }),
  );
  appointmentForm.reset();
});

clearAppointmentsBtn.addEventListener("click", () => {
  setEmptyAppointments();
});

moodButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    moodButtons.forEach((item) => item.classList.remove("active"));
    btn.classList.add("active");
    selectedMood = btn.dataset.mood;
    snapshotMood.textContent = selectedMood;
  });
});

painLevel.addEventListener("input", () => {
  painValue.textContent = painLevel.value;
  snapshotPain.textContent = `${painLevel.value}/10`;
});

energyLevel.addEventListener("input", () => {
  energyValue.textContent = energyLevel.value;
  snapshotEnergy.textContent = `${energyLevel.value}/10`;
});

moodForm.addEventListener("submit", (event) => {
  event.preventDefault();

  if (!selectedMood) {
    return;
  }

  const note = document.getElementById("moodNote").value.trim();
  const time = new Date().toLocaleString();

  const emptyRow = moodHistoryBody.querySelector(".empty-row");
  if (emptyRow) {
    emptyRow.remove();
  }

  const row = document.createElement("tr");
  [
    time,
    selectedMood,
    `${painLevel.value}/10`,
    `${energyLevel.value}/10`,
    note || "No note",
  ].forEach((value) => {
    const cell = document.createElement("td");
    cell.textContent = value;
    row.appendChild(cell);
  });

  moodHistoryBody.prepend(row);
  snapshotNote.textContent = note || "No note saved yet.";
  document.getElementById("moodNote").value = "";
});

clearMoodBtn.addEventListener("click", () => {
  setEmptyMoodHistory();
  snapshotMood.textContent = "Not set";
  snapshotNote.textContent = "No note saved yet.";
  moodButtons.forEach((item) => item.classList.remove("active"));
  selectedMood = "";
});
