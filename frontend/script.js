// // Toggle password visibility for a given input and button
// function setupTogglePassword(toggleId, inputId) {
//   const toggleBtn = document.getElementById(toggleId);
//   const input = document.getElementById(inputId);
//   if (!toggleBtn || !input) return;
//   toggleBtn.addEventListener("click", function () {
//     if (input.type === "password") {
//       input.type = "text";
//       toggleBtn.textContent = "Hide";
//     } else {
//       input.type = "password";
//       toggleBtn.textContent = "Show";
//     }
//   });
// }

// // Registration form toggles
// // Enable show/hide password for registration form
// setupTogglePassword("toggle-reg-password", "reg-password");
// setupTogglePassword("toggle-reg-password2", "reg-password2");
// // Enable show/hide password for login form
// setupTogglePassword("toggle-login-password", "login-password");

// // Smooth form switching
// // Get form and link elements for switching between registration and login
// const registrationForm = document.getElementById("registration-form");
// const loginForm = document.getElementById("login-form");
// const showLogin = document.getElementById("show-login");
// const showRegister = document.getElementById("show-register");

// // When 'Login here' is clicked, fade out registration and fade in login form
// if (showLogin && registrationForm && loginForm) {
//   showLogin.addEventListener("click", function (e) {
//     e.preventDefault();
//     registrationForm.style.opacity = 1;
//     registrationForm.style.transition = "opacity 0.4s";
//     registrationForm.style.opacity = 0;
//     setTimeout(() => {
//       registrationForm.style.display = "none";
//       loginForm.style.display = "block";
//       loginForm.style.opacity = 0;
//       loginForm.style.transition = "opacity 0.4s";
//       setTimeout(() => {
//         loginForm.style.opacity = 1;
//       }, 10);
//     }, 400);
//   });
// }

// // When 'Register here' is clicked, fade out login and fade in registration form
// if (showRegister && registrationForm && loginForm) {
//   showRegister.addEventListener("click", function (e) {
//     e.preventDefault();
//     loginForm.style.opacity = 1;
//     loginForm.style.transition = "opacity 0.4s";
//     loginForm.style.opacity = 0;
//     setTimeout(() => {
//       loginForm.style.display = "none";
//       registrationForm.style.display = "block";
//       registrationForm.style.opacity = 0;
//       registrationForm.style.transition = "opacity 0.4s";
//       setTimeout(() => {
//         registrationForm.style.opacity = 1;
//       }, 10);
//     }, 400);
//   });
// }

// // OTP form
// // Set the email from registration
// document.getElementById("user-email").textContent =
//     localStorage.getItem("userEmail") || "user@example.com";
//       // Only allow numbers in OTP input
// document.getElementById("otp").addEventListener("input", function (e) {
//     this.value = this.value.replace(/[^0-9]/g, "").slice(0, 6);
// });
//       // Resend code click
// document.getElementById("resend").addEventListener("click", function (e) {
//     e.preventDefault();
//     alert("A new code has been sent to your email.");
// });

// Toggle password visibility for a given input and button
function setupTogglePassword(toggleId, inputId) {
  const toggleBtn = document.getElementById(toggleId);
  const input = document.getElementById(inputId);
  if (!toggleBtn || !input) return;
  toggleBtn.addEventListener("click", function () {
    if (input.type === "password") {
      input.type = "text";
      toggleBtn.textContent = "Hide";
    } else {
      input.type = "password";
      toggleBtn.textContent = "Show";
    }
  });
}

// Registration form toggles
setupTogglePassword("toggle-reg-password", "reg-password");
setupTogglePassword("toggle-reg-password2", "reg-password2");
// Login form toggle
setupTogglePassword("toggle-login-password", "login-password");

// OTP form functionality
// Set the email from registration
const userEmailElement = document.getElementById("user-email");
if (userEmailElement) {
  userEmailElement.textContent =
    localStorage.getItem("userEmail") || "user@example.com";
}

// Only allow numbers in OTP input
const otpInput = document.getElementById("otp");
if (otpInput) {
  otpInput.addEventListener("input", function (e) {
    this.value = this.value.replace(/[^0-9]/g, "").slice(0, 6);
  });
}

// Resend code click
const resendBtn = document.getElementById("resend");
if (resendBtn) {
  resendBtn.addEventListener("click", function (e) {
    e.preventDefault();
    alert("A new code has been sent to your email.");
  });
}
