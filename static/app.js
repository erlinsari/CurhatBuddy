const chatWindow = document.getElementById('chat-window');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const themeSelect = document.getElementById('theme-select');
const resetButton = document.getElementById('reset-button');

async function postJson(url, payload) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });
  return response.json();
}

function appendMessage(text, sender) {
  const message = document.createElement('div');
  message.classList.add('message', sender);
  message.textContent = text;
  chatWindow.appendChild(message);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function startConversation() {
  chatWindow.innerHTML = '';
  const theme = themeSelect.value;
  const data = await postJson('/api/start', { theme });
  if (data.reply) {
    appendMessage(data.reply, 'bot');
  }
}

chatForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const message = chatInput.value.trim();
  if (!message) return;
  appendMessage(message, 'user');
  chatInput.value = '';

  const theme = themeSelect.value;
  const data = await postJson('/api/chat', { theme, message });
  if (data.reply) {
    appendMessage(data.reply, 'bot');
  }
});

themeSelect.addEventListener('change', async () => {
  await startConversation();
});

resetButton.addEventListener('click', async () => {
  await startConversation();
});

startConversation();
