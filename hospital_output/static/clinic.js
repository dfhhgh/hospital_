const doctorSearchInput = document.getElementById("doctorSearch");
const doctorFilters = document.querySelectorAll(".doctor-filter");
const doctorCards = document.querySelectorAll("#doctorCards .doctor-card");

function checkedValues(filterName) {
  return Array.from(
    document.querySelectorAll(
      `.doctor-filter[data-filter="${filterName}"]:checked`,
    ),
  ).map((item) => item.value.toLowerCase());
}

function matchesSelected(value, selectedValues) {
  if (selectedValues.length === 0 || selectedValues.includes("all")) {
    return true;
  }
  return selectedValues.includes(value.toLowerCase());
}

function applyDoctorFilters() {
  if (!doctorCards.length) {
    return;
  }

  const term = (doctorSearchInput?.value || "").trim().toLowerCase();
  const departments = checkedValues("department");
  const availability = checkedValues("availability");
  const ratings = checkedValues("rating");
  const genders = checkedValues("gender");

  doctorCards.forEach((card) => {
    const name = (card.dataset.name || "").toLowerCase();
    const department = card.dataset.department || "";
    const available = card.dataset.availability || "";
    const rating = parseFloat(card.dataset.rating || "0");
    const gender = card.dataset.gender || "";

    const matchesTerm =
      !term || name.includes(term) || department.toLowerCase().includes(term);
    const matchesDepartment = matchesSelected(department, departments);
    const matchesAvailability = matchesSelected(available, availability);
    const matchesGender = matchesSelected(gender, genders);

    let matchesRating = true;
    if (ratings.length && !ratings.includes("all")) {
      matchesRating = ratings.some((value) => rating >= parseFloat(value));
    }

    card.classList.toggle(
      "hidden",
      !(
        matchesTerm &&
        matchesDepartment &&
        matchesAvailability &&
        matchesGender &&
        matchesRating
      ),
    );
  });
}

doctorSearchInput?.addEventListener("input", applyDoctorFilters);
doctorFilters.forEach((input) =>
  input.addEventListener("change", applyDoctorFilters),
);

const homeSearchInput = document.getElementById("homeDoctorSearch");
const homeSearchBtn = document.getElementById("homeSearchBtn");
const homeDoctorCards = document.querySelectorAll(
  "#homeDoctorsList .doctor-mini-card",
);

function filterHomeDoctors() {
  const term = (homeSearchInput?.value || "").trim().toLowerCase();
  homeDoctorCards.forEach((card) => {
    const name = (card.dataset.name || "").toLowerCase();
    const specialty = (card.dataset.specialty || "").toLowerCase();
    const show = !term || name.includes(term) || specialty.includes(term);
    card.classList.toggle("hidden", !show);
  });
}

homeSearchBtn?.addEventListener("click", filterHomeDoctors);
homeSearchInput?.addEventListener("input", filterHomeDoctors);

const appointmentLinks = document.querySelectorAll(".book-appointment-link");

function textFrom(card, selector, fallback = "") {
  const node = card.querySelector(selector);
  return node ? node.textContent.trim() : fallback;
}

function buildDoctorQuery(card) {
  const doctor =
    card.dataset.name || textFrom(card, "h3", "Dr. Marcus Johnson");
  const specialty =
    card.dataset.specialty || textFrom(card, ".highlight", "Cardiologist");
  const experience =
    card.dataset.experience ||
    textFrom(card, "p:nth-of-type(2)", "15+ Years Experience");
  const dept =
    card.dataset.dept || textFrom(card, "p:last-of-type", "General Dept.");
  const image = card.dataset.image || card.querySelector("img")?.src || "";

  const params = new URLSearchParams({
    doctor,
    specialty,
    experience,
    dept,
    image,
  });

  return params.toString();
}

appointmentLinks.forEach((link) => {
  const card = link.closest("[data-name]");
  if (!card) {
    return;
  }

  const baseHref = link.getAttribute("href") || "/appointment";
  link.setAttribute("href", `${baseHref}?${buildDoctorQuery(card)}`);
});

const calendarDays = document.getElementById("calendarDays");
const monthLabel = document.getElementById("monthLabel");
const prevMonth = document.getElementById("prevMonth");
const nextMonth = document.getElementById("nextMonth");
const selectedDateInput = document.getElementById("selectedDate");
const selectedTimeInput = document.getElementById("selectedTime");
const timeButtons = document.querySelectorAll("#timeSlots button");
const bookingForm = document.getElementById("bookingForm");
const bookingResult = document.getElementById("bookingResult");
const bookingDoctorName = document.getElementById("bookingDoctorName");
const bookingDoctorSpecialty = document.getElementById(
  "bookingDoctorSpecialty",
);
const bookingDoctorExperience = document.getElementById(
  "bookingDoctorExperience",
);
const bookingDoctorDepartment = document.getElementById(
  "bookingDoctorDepartment",
);
const bookingDoctorImage = document.getElementById("bookingDoctorImage");

function applySelectedDoctorToBooking() {
  if (!bookingDoctorName) {
    return;
  }

  const params = new URLSearchParams(window.location.search);
  const doctor = params.get("doctor");
  const specialty = params.get("specialty");
  const experience = params.get("experience");
  const dept = params.get("dept");
  const image = params.get("image");

  if (doctor) {
    bookingDoctorName.textContent = doctor;
  }
  if (specialty) {
    bookingDoctorSpecialty.textContent = specialty;
  }
  if (experience) {
    bookingDoctorExperience.textContent = experience;
  }
  if (dept) {
    bookingDoctorDepartment.textContent = dept;
  }
  if (image && bookingDoctorImage) {
    bookingDoctorImage.src = image;
    bookingDoctorImage.alt = doctor || "Selected doctor";
  }
}

let currentDate = new Date();
let selectedDay = currentDate.getDate();

function formatDisplayDate(date) {
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
}

function renderCalendar() {
  if (!calendarDays || !monthLabel) {
    return;
  }

  calendarDays.innerHTML = "";

  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();
  const firstDayIndex = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const daysInPrevMonth = new Date(year, month, 0).getDate();

  monthLabel.textContent = currentDate.toLocaleDateString("en-US", {
    month: "long",
    year: "numeric",
  });

  for (let i = firstDayIndex - 1; i >= 0; i -= 1) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "muted";
    btn.textContent = String(daysInPrevMonth - i);
    calendarDays.appendChild(btn);
  }

  for (let day = 1; day <= daysInMonth; day += 1) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = String(day);
    btn.classList.add("current");

    if (day === selectedDay) {
      btn.classList.add("selected");
      selectedDateInput.value = formatDisplayDate(new Date(year, month, day));
    }

    btn.addEventListener("click", () => {
      selectedDay = day;
      selectedDateInput.value = formatDisplayDate(new Date(year, month, day));
      renderCalendar();
    });

    calendarDays.appendChild(btn);
  }
}

prevMonth?.addEventListener("click", () => {
  currentDate = new Date(
    currentDate.getFullYear(),
    currentDate.getMonth() - 1,
    1,
  );
  selectedDay = 1;
  renderCalendar();
});

nextMonth?.addEventListener("click", () => {
  currentDate = new Date(
    currentDate.getFullYear(),
    currentDate.getMonth() + 1,
    1,
  );
  selectedDay = 1;
  renderCalendar();
});

timeButtons.forEach((button) => {
  button.addEventListener("click", () => {
    timeButtons.forEach((item) => item.classList.remove("selected"));
    button.classList.add("selected");
    selectedTimeInput.value = button.dataset.time || "";
  });
});

bookingForm?.addEventListener("submit", (event) => {
  event.preventDefault();

  const fullName = document.getElementById("fullName")?.value.trim();
  const emailAddress = document.getElementById("emailAddress")?.value.trim();
  const visitReason = document.getElementById("visitReason")?.value.trim();

  if (!fullName || !emailAddress || !visitReason) {
    return;
  }

  const finalDate = selectedDateInput.value || formatDisplayDate(new Date());
  const finalTime = selectedTimeInput.value || "10:30 AM";
  const doctorNameForBooking =
    bookingDoctorName?.textContent?.trim() || "your selected doctor";

  bookingResult.textContent = `Booking confirmed with ${doctorNameForBooking} for ${fullName} on ${finalDate} at ${finalTime}.`;
  bookingForm.reset();
  selectedTimeInput.value = "10:30 AM";

  timeButtons.forEach((button) => {
    const active = button.dataset.time === "10:30 AM";
    button.classList.toggle("selected", active);
  });
});

const contactForm = document.getElementById("contactForm");
const contactResult = document.getElementById("contactResult");

contactForm?.addEventListener("submit", (event) => {
  event.preventDefault();

  const contactName = document.getElementById("contactName")?.value.trim();
  if (!contactName) {
    return;
  }

  contactResult.textContent = `Thanks ${contactName}, your message has been sent successfully.`;
  contactForm.reset();
});

applySelectedDoctorToBooking();
renderCalendar();
