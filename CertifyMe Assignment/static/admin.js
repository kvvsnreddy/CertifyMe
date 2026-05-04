const email = document.getElementById('loginEmail').value.trim();
const password = document.getElementById('loginPassword').value.trim();

fetch('/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
})
.then(res => res.json())
.then(data => {
    if (data.message === "Login successful") {
        showToast('Welcome ' + data.user);
        showDashboard(email);
    } else {
        showToast('Error: ' + data.message);
    }
});
