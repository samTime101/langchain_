import { useState } from "react";

function App() {
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const getWeather = () => {
    setLoading(true);
    setError("");

    if (!navigator.geolocation) {
      setError("Geolocation is not supported by your browser.");
      setLoading(false);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        try {
          const latitude = position.coords.latitude;
          const longitude = position.coords.longitude;

          const locationResponse = await fetch(
            `https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`
          );

          const locationData = await locationResponse.json();

          const city =
            locationData.address.city ||
            locationData.address.town ||
            locationData.address.village;

          if (!city) {
            throw new Error("Could not determine city");
          }

          const response = await fetch(
            "http://127.0.0.1:8000/weather",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                city: city,
              }),
            }
          );

          if (!response.ok) {
            throw new Error("Weather API failed");
          }

          const data = await response.json();

          setWeather(data);
        } catch (err) {
          setError(err.message);
        } finally {
          setLoading(false);
        }
      },
      (error) => {
        setError("Please allow location access.");
        setLoading(false);
      }
    );
  };

  return (
    <div style={{ padding: "40px", maxWidth: "600px", margin: "auto" }}>
      <h1>Weather Agent</h1>

      <button onClick={getWeather} disabled={loading}>
        {loading ? "Getting Weather..." : "Get My Weather"}
      </button>

      {error && (
        <p style={{ color: "red" }}>
          {error}
        </p>
      )}

      {weather && (
        <div style={{ marginTop: "30px" }}>
          <h2>{weather.city}</h2>

          <p>{weather.summary}</p>

          <p>
            Celsius: {weather.temperature_celsius}
          </p>

          <p>
            Fahrenheit: {weather.temperature_fahrenheit}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;