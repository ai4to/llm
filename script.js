async function askChatGPT() {
  const userInput = document.getElementById("input").value;
  const output = document.getElementById("output");
  output.textContent = "Thinking...";

  try {
    const res = await fetch("https://llm-jlil.onrender.com/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userInput }),
    });

    const data = await res.json();
    output.textContent = data?.choices?.[0]?.message?.content || "No response.";
  } catch (err) {
    output.textContent = "Error: " + err.message;
  }
}
