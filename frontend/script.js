const chatbotButton = document.getElementById('chatbot-button');
const chatbotBox = document.getElementById('chatbot-box');

chatbotButton.onclick = () => {
  if (chatbotBox.style.display === 'flex') {
    chatbotBox.style.display = 'none';
  } else {
    chatbotBox.style.display = 'flex';
  }
};

async function sendMessage() {
  const input = document.getElementById('user-input');
  const chatLog = document.getElementById('chat-log');
  const userText = input.value.trim();
  if (!userText) return;

//   chatLog.innerHTML += `<div><strong>You:</strong> ${userText}</div>`;
    chatLog.innerHTML += `<div class="chat-message user"><strong>You:</strong> ${userText}</div>`;

  input.value = "";

  try {
    const res = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userText })
    });

    const data = await res.json();
    // chatLog.innerHTML += `<div><strong>AI:</strong> ${data.response}</div>`;
    chatLog.innerHTML += `<div class="chat-message ai"><strong>AI:</strong> ${data.response}</div>`;
  } catch (err) {
    chatLog.innerHTML += `<div><strong>AI:</strong> Sorry, I couldn’t connect to the server.</div>`;
  }

  chatLog.scrollTop = chatLog.scrollHeight;
}
