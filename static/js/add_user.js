// This file to add username to common list

async function sendName() {
    const name = prompt("Please enter your name:");
    if (name) {
        const response = await fetch('http://127.0.0.1:8000/add_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: name })
        });
        const result = await response.json();
    }
}
