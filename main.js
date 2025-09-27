const socket = io();

socket.on('response', function(data) {
    const messagesDiv = document.getElementById('messages');
    const p = document.createElement('p');
    p.textContent = data.msg;
    messagesDiv.appendChild(p);
});

function sendMessage() {
    const input = document.getElementById('userInput');
    socket.emit('message', { text: input.value });
    input.value = '';
}

// Chart initialization
const ctx = document.getElementById('cooperativeChart').getContext('2d');
const cooperativeChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Emergent Cooperative Index'],
        datasets: [{
            label: 'Index Value',
            data: [85],
            backgroundColor: ['#2b8732']
        }]
    },
    options: {
        scales: {
            y: { beginAtZero: true, max: 100 }
        }
    }
});
