function setupTogglePassword(toggleId, inputId) {
  const toggleBtn = document.getElementById(toggleId);
  const input = document.getElementById(inputId);
  
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

setupTogglePassword("toggle-password", "password");
setupTogglePassword("toggle-password2", "password2");
