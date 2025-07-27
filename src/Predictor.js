import React, { useState } from "react";

function PredictForm() {
  const [formData, setFormData] = useState({
    Nitrogen: 36,
    Phosphorus: 32,
    Potassium: 50,
    Temperature: 5,
    Humidity: 70,
    PH: 3,
    Rainfall: 200,
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: parseFloat(e.target.value) });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <h2>Crop Prediction Form</h2>
      <form onSubmit={handleSubmit}>
        {Object.entries(formData).map(([key, value]) => (
          <div key={key}>
            <label>{key}:</label>
            <input
              type="number"
              name={key}
              value={value}
              onChange={handleChange}
              min="1"
              max="500"
              step="any"
              required
            />
          </div>
        ))}
        <button type="submit">Predict</button>
      </form>

      {result && (
        <div>
          <h3>Prediction Result</h3>
          <p>
            <strong>Predicted Crop:</strong> {result.predicted_category}
          </p>
          <p>
            <strong>Confidence:</strong> {result.confidence}
          </p>
          <h4>Class Probabilities:</h4>
          <ul>
            {Object.entries(result.class_probabilities).map(([crop, prob]) => (
              <li key={crop}>
                {crop}: {prob}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default PredictForm;
