// 1. Send OTP
document.getElementById("sendOtpBtn").addEventListener("click", async () => {
  const mobile = document.getElementById("mobile").value;
  await fetch("http://127.0.0.1:5000/send_otp", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ mobile }),
  });
  alert("OTP sent! Check console for OTP (for testing).");
});

// 2. Verify OTP & Register
document.getElementById("registerBtn").addEventListener("click", async () => {
  const name = document.getElementById("name").value;
  const mobile = document.getElementById("mobile").value;
  const password = document.getElementById("password").value;
  const otp = document.getElementById("otp").value;

  const response = await fetch("http://127.0.0.1:5000/verify_register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, mobile, password, otp }),
  });

  const data = await response.json();
  alert(data.message);
});
