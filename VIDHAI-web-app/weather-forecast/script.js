/* const inputBox = document.querySelector(".input-box");
const searchBtn = document.getElementById("searchBtn");
const weather_img = document.querySelector(".weather-img");
const temperature = document.querySelector(".temperature");
const description = document.querySelector(".description");
const humidity = document.getElementById("humidity");
const wind_speed = document.getElementById("wind-speed");

const location_not_found = document.querySelector(".location-not-found");

const weather_body = document.querySelector(".weather-body");

async function checkWeather(city) {
  const api_key = "4c4286de4f6a3794841e570fd8bc4a0b";
  const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${api_key}`;

  const weather_data = await fetch(`${url}`).then((response) =>
    response.json()
  );

  if (weather_data.cod === `404`) {
    location_not_found.style.display = "flex";
    weather_body.style.display = "none";
    console.log("error");
    return;
  }

  console.log("run");
  location_not_found.style.display = "none";
  weather_body.style.display = "flex";
  temperature.innerHTML = `${Math.round(weather_data.main.temp - 273.15)}°C`;
  description.innerHTML = `${weather_data.weather[0].description}`;

  humidity.innerHTML = `${weather_data.main.humidity}%`;
  wind_speed.innerHTML = `${weather_data.wind.speed}Km/H`;

  switch (weather_data.weather[0].main) {
    case "Clouds":
      weather_img.src = "img/cloud.png";
      break;
    case "Clear":
      weather_img.src = "img/clear-sky.png";
      break;
    case "Rain":
      weather_img.src = "img/rain.png";
      break;
    case "Haze":
      weather_img.src = "img/haze.png";
      break;
    case "Lightning":
      weather_img.src = "img/lightning.png";
      break;
    case "Snow":
      weather_img.src = "img/snow.png";
      break;
    case "Storm":
      weather_img.src = "img/storm.png";
      break;
    case "Thunderstorm":
      weather_img.src = "img/thunderstorm.png";
      break;
    case "Mist":
      weather_img.src = "img/mist.png";
      break;
    case "Snow":
      weather_img.src = "img/snow.png";
      break;
  }

  console.log(weather_data);
}

searchBtn.addEventListener("click", () => {
  checkWeather(inputBox.value);
});

// 🎤 Voice Recognition (Malayalam ➡ English)
const micBtn = document.getElementById("micBtn");
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
  const recognition = new SpeechRecognition();
  recognition.lang = "ml-IN"; // Malayalam speech
  recognition.interimResults = false;

  micBtn.addEventListener("click", () => {
    recognition.start();
  });




  //new 
  recognition.onresult = async (event) => {
    const spokenText = event.results[0][0].transcript;
    console.log("Malayalam Speech:", spokenText);

    // Malayalam ➡ English translate (LibreTranslate உதாரணம்)
    const response = await fetch(
      "https://translate.argosopentech.com/translate",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          q: "ചെന്നൈ",
          source: "ml",
          target: "en",
          format: "text",
        }),
      }
    )
      .then((r) => r.json())
      .then(console.log)
      .catch(console.error);

    const data = await response.json();
    const translatedText = data.translatedText;
    console.log("Translated to English:", translatedText);

    inputBox.value = translatedText;
    checkWeather(translatedText);
  };
} else {
  alert("Speech Recognition not supported in this browser.");
}
 */

// script.js (copy this completely)
const inputBox = document.querySelector(".input-box");
const searchBtn = document.getElementById("searchBtn");
const micBtn = document.getElementById("micBtn"); // make sure exists in HTML
const weather_img = document.querySelector(".weather-img");
const temperature = document.querySelector(".temperature");
const description = document.querySelector(".description");
const humidity = document.getElementById("humidity");
const wind_speed = document.getElementById("wind-speed");
const location_not_found = document.querySelector(".location-not-found");
const weather_body = document.querySelector(".weather-body");

// -------------- Translation function (uses argos instance) --------------
async function translateMalayalamToEnglish(text) {
  try {
    console.log("Translating:", text);
    const res = await fetch("https://translate.argosopentech.com/translate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        q: text,
        source: "ml",
        target: "en",
        format: "text",
      }),
    });

    if (!res.ok) {
      console.error("Translate API status:", res.status);
      return null;
    }

    const data = await res.json();
    console.log("Translation response:", data);

    // common successful property is translatedText
    if (data && data.translatedText) return data.translatedText;
    // fallback for other property names
    if (data && (data.result || data.translation))
      return data.result || data.translation;

    return null;
  } catch (err) {
    console.error("Translate error:", err);
    return null;
  }
}

// -------------- Weather fetch function --------------
async function checkWeather(city) {
  if (!city || !city.trim()) {
    alert("Please enter a city name.");
    return;
  }

  const api_key = "4c4286de4f6a3794841e570fd8bc4a0b"; // for testing only
  const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(
    city
  )}&appid=${api_key}`;

  try {
    const res = await fetch(url);
    if (!res.ok) {
      console.error("Weather API status:", res.status);
      // show not found UI for 404; generic message for others
      location_not_found.style.display = "flex";
      weather_body.style.display = "none";
      const text = await res.text();
      console.log("Weather API body:", text);
      return;
    }

    const weather_data = await res.json();
    if (!weather_data || !weather_data.main || !weather_data.weather) {
      console.error("Invalid weather response:", weather_data);
      location_not_found.style.display = "flex";
      weather_body.style.display = "none";
      return;
    }

    // display data
    location_not_found.style.display = "none";
    weather_body.style.display = "flex";
    temperature.innerHTML = `${Math.round(weather_data.main.temp - 273.15)}°C`;
    description.innerHTML = `${weather_data.weather[0].description}`;
    humidity.innerHTML = `${weather_data.main.humidity}%`;
    wind_speed.innerHTML = `${weather_data.wind.speed}Km/H`;

    const w = weather_data.weather[0].main;
    switch (w) {
      case "Clouds":
        weather_img.src = "img/cloud.png";
        break;
      case "Clear":
        weather_img.src = "img/clear-sky.png";
        break;
      case "Rain":
        weather_img.src = "img/rain.png";
        break;
      case "Haze":
        weather_img.src = "img/haze.png";
        break;
      case "Lightning":
        weather_img.src = "img/lightning.png";
        break;
      case "Snow":
        weather_img.src = "img/snow.png";
        break;
      case "Storm":
        weather_img.src = "img/storm.png";
        break;
      case "Thunderstorm":
        weather_img.src = "img/thunderstorm.png";
        break;
      case "Mist":
        weather_img.src = "img/mist.png";
        break;
      default:
        weather_img.src = "img/cloud.png";
    }

    console.log("Weather data:", weather_data);
  } catch (err) {
    console.error("Fetch weather failed:", err);
    location_not_found.style.display = "flex";
    weather_body.style.display = "none";
  }
}

searchBtn.addEventListener("click", () => {
  checkWeather(inputBox.value);
});

// ✅ --- Add this after searchBtn.addEventListener ---
window.SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

if ("SpeechRecognition" in window) {
  const recognition = new SpeechRecognition();
  recognition.lang = "en-US"; // English only
  recognition.interimResults = false;

  // Start listening when mic button is clicked
  micBtn.addEventListener("click", () => {
    recognition.start();
    micBtn.textContent = "🎙️ Listening...";
  });

  // When speech is recognized
  recognition.addEventListener("result", (e) => {
    const transcript = e.results[0][0].transcript;
    inputBox.value = transcript; // Fill input with recognized text
    checkWeather(transcript); // Automatically fetch weather
  });

  // Reset mic button text when done
  recognition.addEventListener("end", () => {
    micBtn.textContent = "🎙️";
  });
} else {
  // If browser doesn’t support speech recognition
  micBtn.addEventListener("click", () => {
    alert("Speech recognition is not supported in this browser.");
  });
}
