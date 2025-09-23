document.getElementById('send-message').addEventListener('click', async function() {
  const userMessage = document.getElementById('user-input').value.trim();
  if (!userMessage) return;

  const chatWindow = document.getElementById('chat');
  
  // Display user message
  const userMessageElement = document.createElement('div');
  userMessageElement.textContent = 'You: ' + userMessage;
  userMessageElement.className = 'user-message';
  chatWindow.appendChild(userMessageElement);

  // Show loading status
  const loadingElement = document.createElement('div');
  loadingElement.textContent = 'Euystacio is thinking...';
  loadingElement.className = 'ai-message';
  chatWindow.appendChild(loadingElement);

  // Replace with your actual backend URL
  const apiUrl = "http://localhost:5000/api/reflect"; // API endpoint for reflection

  try {
    // Sending the user message to the backend for processing
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: userMessage }), // Send the message as JSON
    });

    const data = await response.json();

    // Check if the response is valid
    if (data && data.reflection) {
      // Display the AI (kernel) response
      const aiMessageElement = document.createElement('div');
      aiMessageElement.textContent = 'Euystacio: ' + data.reflection;
      aiMessageElement.className = 'ai-message';
      chatWindow.appendChild(aiMessageElement);
    } else {
      // If no response or error, show a fallback message
      loadingElement.textContent = 'Euystacio couldn\'t respond at the moment.';
    }
  } catch (error) {
    console.error('Error with the chat interaction:', error);
    loadingElement.textContent = 'An error occurred. Please try again later.';
  }

  // Clear the input and scroll the chat window
  document.getElementById('user-input').value = '';
  chatWindow.scrollTop = chatWindow.scrollHeight;
});