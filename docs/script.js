document.getElementById('send-message').addEventListener('click', async function() {
  const userMessage = document.getElementById('user-input').value.trim();
  if (!userMessage) return;

  const chatWindow = document.getElementById('chat');
  
  // Display user message
  const userMessageElement = document.createElement('div');
  userMessageElement.classList.add('user-message');
  userMessageElement.textContent = 'You: ' + userMessage;
  chatWindow.appendChild(userMessageElement);

  // Show loading status
  const loadingElement = document.createElement('div');
  loadingElement.classList.add('ai-message');
  loadingElement.textContent = 'Euystacio is thinking...';
  chatWindow.appendChild(loadingElement);

  // API URL for sending the pulse (message)
  const pulseApiUrl = "http://localhost:5000/api/pulse"; // Replace with live API URL

  try {
    // Send pulse to Euystacio
    const pulseResponse = await fetch(pulseApiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ pulse: userMessage }), // Sending the pulse (message)
    });

    const pulseData = await pulseResponse.json();

    // Remove loading state
    chatWindow.removeChild(loadingElement);

    if (pulseData && pulseData.response) {
      // Display AI response from Euystacio
      const aiMessageElement = document.createElement('div');
      aiMessageElement.classList.add('ai-message');
      aiMessageElement.textContent = 'Euystacio: ' + pulseData.response;
      chatWindow.appendChild(aiMessageElement);
    } else {
      const errorElement = document.createElement('div');
      errorElement.classList.add('ai-message');
      errorElement.textContent = 'No response from Euystacio. Please try again.';
      chatWindow.appendChild(errorElement);
    }

    // Fetch harmony level from system status
    const statusApiUrl = "http://localhost:5000/api/system_status"; // Replace with live API URL
    const statusResponse = await fetch(statusApiUrl);
    const statusData = await statusResponse.json();

    // Extract harmony level from system status
    const harmonyLevel = statusData.harmony_level || 'Unknown';

    // Display the harmony level
    const harmonyElement = document.createElement('div');
    harmonyElement.classList.add('ai-message');
    harmonyElement.textContent = `Harmony Level: ${harmonyLevel}`;
    chatWindow.appendChild(harmonyElement);

  } catch (error) {
    console.error('Error with the pulse interaction:', error);
    chatWindow.removeChild(loadingElement);
    const errorElement = document.createElement('div');
    errorElement.classList.add('ai-message');
    errorElement.textContent = 'An error occurred. Please try again later.';
    chatWindow.appendChild(errorElement);
  }

  // Clear the input and scroll to the bottom of the chat
  document.getElementById('user-input').value = '';
  chatWindow.scrollTop = chatWindow.scrollHeight;
});
