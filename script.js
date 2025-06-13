async function sendMessage() {
  const input = document.getElementById('userInput').value;
  const output = document.getElementById('responseOutput');
  output.textContent = "Loading...";

  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer YOUR_API_KEY"  // NEVER EXPOSE THIS PUBLICLY!
    },
    body: JSON.stringify({
      model: "gpt-3.5-turbo",
      messages: [{ role: "user", content: input }],
    }),
  });

  const data = await response.json();
  output.textContent = data.choices?.[0]?.message?.content || "Error.";
}
