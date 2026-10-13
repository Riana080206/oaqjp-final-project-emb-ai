async function RunSentimentAnalysis() {
    const text = document.getElementById("textToAnalyze").value;
    const resultArea = document.getElementById("system_response");

    if (!text.trim()) {
        resultArea.innerText = "Please enter some text to analyze.";
        return;
    }

    resultArea.innerText = "Analyzing...";

    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000);

        try {
            const response = await fetch(
                "/emotionDetector?textToAnalyze=" + encodeURIComponent(text),
                { signal: controller.signal }
            );

            const data = await response.text();

            if (!response.ok) {
                throw new Error(data);
            }

            resultArea.innerText = data;
        } finally {
            clearTimeout(timeoutId);
        }
    } catch (error) {
        resultArea.innerText = error.name === "AbortError"
            ? "Request timed out. The emotion service may be unavailable."
            : "Detection failed: " + error.message;
    }
}