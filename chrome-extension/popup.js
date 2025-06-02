document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("checkButton").addEventListener("click", async () => {
        const text = document.getElementById("textInput").value.trim();

        if (!text) {
            document.getElementById("result").innerText = "⚠️ Please enter some text.";
            return;
        }

        document.getElementById("result").innerText = "Analyzing...";

        try {
            const response = await fetch("https://your-render-api-url.onrender.com/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: text })
            });

            const data = await response.json();

            document.getElementById("result").innerText =
                data.predicted_labels.includes("Safe")
                    ? "✅ Safe comment!"
                    : "🚨 Toxic: " + data.predicted_labels.join(", ");
        } catch (error) {
            console.error("Error contacting backend:", error);
            document.getElementById("result").innerText = "❌ Error connecting to server.";
        }
    });
});
