document
  .getElementById("user-input")
  .addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.altKey) {
      this.style.height = "";
      event.preventDefault(); // Prevents the default Enter key behavior
      sendMessage();
    } else if (event.key === "Enter" && event.altKey) {
      // Insert a new line in the input field when Alt + Enter is pressed
      const cursorPosition = this.selectionStart;
      const textBeforeCursor = this.value.substring(0, cursorPosition);
      const textAfterCursor = this.value.substring(cursorPosition);
      this.value = textBeforeCursor + "\n" + textAfterCursor;
      this.selectionEnd = cursorPosition + 1; // Move the cursor to the next line
      this.style.height = this.scrollHeight + "px";
    }
  });

function uploadPdf() {
  let url = document.getElementById("pdf-url").value;
  const logBox = document.getElementById("pdf-log");
  if (url == "") {
    logBox.innerHTML = "Please enter a valid PDF URL";
  } else {
    logBox.innerHTML = "Reading Your PDF <br> Please wait for a while...";
    fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: url }),
    })
      .then((response) => response.json())
      .then((data) => {
        // Create log response
        logBox.innerHTML = data.response;
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
}

let canSendMessage = true;
function sendMessage() {
  if (canSendMessage) {
    canSendMessage = false
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    // Create user message
    const userMessage = document.createElement("div");
    userMessage.classList.add("message", "user-message");
    userMessage.innerText = userInput.value;
    chatBox.appendChild(userMessage);

    const botMessage = document.createElement("div");
    botMessage.classList.add("message", "bot-message");
    botMessage.innerHTML = "Wait AI is responding...";
    chatBox.appendChild(botMessage);

    // Send user input to Flask API
    fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userInput.value }),
    })
      .then((response) => response.json())
      .then((data) => {
        botMessage.innerHTML = data.response;
        // Scroll to bottom
        chatBox.scrollTop = chatBox.scrollHeight;
        canSendMessage = true;
      })
      .catch((error) => {
        console.error("Error:", error);
        canSendMessage=true;
      });

    // Clear input field
    userInput.value = "";
  }
}
