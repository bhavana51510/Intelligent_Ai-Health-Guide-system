let userLocation = null;

/* =========================================================
   UTIL: Smooth Scroll to Results
========================================================= */
function scrollToResults() {
  const section = document.getElementById("results-section");
  if (section) {
    section.scrollIntoView({ behavior: "smooth" });
  }
}

/* =========================================================
   Get User Location
========================================================= */
function getLocation() {

  if (!navigator.geolocation) {
    alert("Geolocation not supported by this browser.");
    return;
  }

  const statusEl = document.getElementById("location-status");
  statusEl.innerText = "Detecting location...";

  navigator.geolocation.getCurrentPosition(
    (pos) => {
      userLocation = {
        lat: pos.coords.latitude,
        lon: pos.coords.longitude
      };
      statusEl.innerText = "Location detected.";
    },
    (err) => {
      console.error(err);
      statusEl.innerText = "Location access denied.";
      alert("Location permission is required.");
    }
  );
}


/* =========================================================
   Loader
========================================================= */
function showLoader() {

  const results = document.getElementById("results");
  const firstAid = document.getElementById("first-aid-section");

  firstAid.style.display = "none";

  results.innerHTML = `
    <div class="loader">
      AI analyzing request...
    </div>
  `;

  scrollToResults();
}


/* =========================================================
   Analyze Text Symptoms
========================================================= */
async function analyze() {

  const symptoms = document.getElementById("symptoms").value.trim();

  if (!symptoms) {
    alert("Please enter symptoms first.");
    return;
  }

  if (!userLocation) {
    alert("Please detect your location first.");
    return;
  }

  showLoader();

  const payload = {
    symptoms,
    latitude: userLocation.lat,
    longitude: userLocation.lon
  };

  try {

    const res = await fetch("/api/full-recommendation", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || "Server error");
    }

    renderResults(data);

  } catch (err) {
    console.error("TEXT API ERROR:", err);
    alert("Server error. Please try again.");
  }
}


/* =========================================================
   Render Results
========================================================= */
function renderResults(data) {

  const categoryEl = document.getElementById("category-title");

  const severityClass = data.severity
    ? data.severity.toLowerCase().replace(" ", "-")
    : "consult-doctor";

  const severityText = data.severity || "Consult Doctor";

  categoryEl.innerHTML = `
    <span class="dept-badge">${data.predicted_category}</span>
    <span class="severity-badge ${severityClass}">
      ${severityText}
    </span>
  `;

  renderFirstAid(data.first_aid);
  renderHospitals(data.hospitals);

  scrollToResults();
}


/* =========================================================
   Render First Aid
========================================================= */
function renderFirstAid(steps) {

  const section = document.getElementById("first-aid-section");
  const list = document.getElementById("first-aid-list");

  if (!steps || steps.length === 0) {
    section.style.display = "none";
    return;
  }

  list.innerHTML = "";

  steps.forEach(step => {
    const li = document.createElement("li");
    li.textContent = step;
    list.appendChild(li);
  });

  section.style.display = "block";
}


/* =========================================================
   Render Hospitals
========================================================= */
function renderHospitals(hospitals) {

  const container = document.getElementById("results");
  container.innerHTML = "";

  if (!hospitals || hospitals.length === 0) {
    container.innerHTML = `
      <div class="hospital-card">
        <p>No hospitals found nearby.</p>
      </div>
    `;
    return;
  }

  hospitals.forEach(h => {

    const card = document.createElement("div");
    card.className = "hospital-card";

    const origin = userLocation
      ? `${userLocation.lat},${userLocation.lon}`
      : "";

    const directionsUrl =
      `https://www.google.com/maps/dir/?api=1` +
      (origin ? `&origin=${origin}` : "") +
      `&destination=${encodeURIComponent(
        `${h.hospital_name}, ${h.area}, ${h.city}`
      )}` +
      "&travelmode=driving";

    card.innerHTML = `
      <h3>${h.hospital_name}</h3>
      <p><strong>Location:</strong> ${h.area}, ${h.city}</p>
      <p><strong>Phone:</strong> ${h.phone || "Not Available"}</p>

      <hr>

      <div class="doctor-section">
        <strong>Available Doctors:</strong>
        <ul>
          ${
            h.doctors && h.doctors.length
              ? h.doctors.map(d =>
                  `<li>${d.doctor_name} — ${d.experience_years} yrs — ₹${d.consultation_fee}</li>`
                ).join("")
              : "<li>No doctor information available</li>"
          }
        </ul>
      </div>

      <div class="map-embed">
        <iframe
          width="100%"
          height="220"
          loading="lazy"
          allowfullscreen
          src="https://www.google.com/maps?q=${encodeURIComponent(
            `${h.hospital_name}, ${h.area}, ${h.city}`
          )}&output=embed">
        </iframe>
      </div>

      <a href="${directionsUrl}" target="_blank" class="map-btn">
        Open in Google Maps
      </a>
    `;

    container.appendChild(card);
  });
}


/* =========================================================
   Image Upload
========================================================= */
async function uploadImage() {

  const fileInput = document.getElementById("imageUpload");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select an image.");
    return;
  }

  if (!userLocation) {
    alert("Please detect your location first.");
    return;
  }

  showLoader();

  const preview = document.getElementById("preview");
  preview.innerHTML =
    `<img src="${URL.createObjectURL(file)}" width="250">`;

  const formData = new FormData();
  formData.append("image", file);
  formData.append("latitude", userLocation.lat);
  formData.append("longitude", userLocation.lon);

  try {

    const res = await fetch("/api/image-upload", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || "Upload failed");
    }

    renderResults({
      predicted_category: data.predicted_category,
      severity: data.severity,
      first_aid: data.first_aid,
      hospitals: data.hospitals
    });

  } catch (err) {
    console.error("IMAGE UPLOAD ERROR:", err);
    alert("Image upload failed.");
  }
}