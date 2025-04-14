async function sendPrompt() {
    const prompt = document.getElementById('prompt').value;
  
    const res = await fetch('http://127.0.0.1:8000/api/gpt', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ prompt })
    });
  
    const data = await res.json();
    document.getElementById('response').innerText = data.response || data.error;
  }
  