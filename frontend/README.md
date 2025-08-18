# HTML, CSS, and JavaScript Explained

Welcome! This guide explains the main parts of your project line by line, so you can learn and understand how everything works.

---

## 1. HTML (index.html)

### Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>User Registration</title>
    <link rel="stylesheet" href="style.css" />
    <script defer src="script.js"></script>
</head>
<body>
    <div class="container">
        <!-- Registration Form -->
        <form id="registration-form" autocomplete="off">
            <h1>User Registration</h1>
            <!-- Input fields for name, username, email, password, confirm password -->
            <!-- Show/Hide password buttons -->
            <button type="submit" id="submit">Sign Up</button>
            <p>Already have an account? <a href="#" id="show-login">Login here</a></p>
        </form>
        <!-- Login Form (hidden by default) -->
        <form id="login-form" autocomplete="off" style="display:none;">
            <h1>User Login</h1>
            <!-- Input fields for username and password -->
            <!-- Show/Hide password button -->
            <button type="submit" id="login-btn">Login</button>
            <p>Don't have an account? <a href="#" id="show-register">Register here</a></p>
        </form>
    </div>
</body>
</html>
```

### Explanation
- `<!DOCTYPE html>`: Declares this is an HTML5 document.
- `<html lang="en">`: Starts the HTML document, sets language to English.
- `<head>`: Contains meta info, title, links to CSS and JS files.
- `<body>`: All visible content goes here.
- `.container`: Centers and contains the forms.
- `form`: Used for user input. Registration and login forms are separate.
- `input`: Fields for user data (name, username, email, password).
- `button`: For submitting forms and toggling password visibility.
- `<a>`: Links to switch between registration and login forms.

---

## 2. CSS (style.css)

### Structure
```css
body {
  background: linear-gradient(135deg, #e8eaf6 0%, #c5cae9 100%);
  font-family: "Poppins", sans-serif;
  margin: 0;
}

.container {
  max-width: 500px;
  margin: 8vh auto 0;
  padding: 0 16px;
}

form {
  background: #fff;
  border-radius: 10px;
  font-size: 14px;
  box-shadow: 0 2px 12px rgba(109, 109, 234, 0.1);
  padding: 32px 24px 24px 24px;
  box-sizing: border-box;
}

.input-control input {
  border: 2px solid #f0f0f0;
  border-radius: 6px;
  font-size: 17px;
  width: 100%;
  padding: 10px 14px;
  background: #f9f9fc;
  box-sizing: border-box;
}
```

### Explanation
- `body`: Sets background color and font for the whole page.
- `.container`: Centers the forms and sets max width.
- `form`: Styles the form box (background, rounded corners, shadow, padding).
- `.input-control input`: Styles the input fields (border, padding, width, rounded corners).
- `box-sizing: border-box`: Ensures padding/border are included in width.

---

## 3. JavaScript (script.js)

### Structure
```javascript
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

// Smooth form switching
const registrationForm = document.getElementById("registration-form");
const loginForm = document.getElementById("login-form");
const showLogin = document.getElementById("show-login");
const showRegister = document.getElementById("show-register");

if (showLogin && registrationForm && loginForm) {
  showLogin.addEventListener("click", function (e) {
    e.preventDefault();
    registrationForm.style.opacity = 1;
    registrationForm.style.transition = "opacity 0.4s";
    registrationForm.style.opacity = 0;
    setTimeout(() => {
      registrationForm.style.display = "none";
      loginForm.style.display = "block";
      loginForm.style.opacity = 0;
      loginForm.style.transition = "opacity 0.4s";
      setTimeout(() => { loginForm.style.opacity = 1; }, 10);
    }, 400);
  });
}

if (showRegister && registrationForm && loginForm) {
  showRegister.addEventListener("click", function (e) {
    e.preventDefault();
    loginForm.style.opacity = 1;
    loginForm.style.transition = "opacity 0.4s";
    loginForm.style.opacity = 0;
    setTimeout(() => {
      loginForm.style.display = "none";
      registrationForm.style.display = "block";
      registrationForm.style.opacity = 0;
      registrationForm.style.transition = "opacity 0.4s";
      setTimeout(() => { registrationForm.style.opacity = 1; }, 10);
    }, 400);
  });
}
```

### Explanation
- `setupTogglePassword`: Sets up the show/hide password button for each input.
- `addEventListener`: Listens for button clicks to toggle password visibility.
- `Smooth form switching`: Shows/hides registration and login forms with a fade effect.
- `preventDefault()`: Stops the link from reloading the page.
- `setTimeout`: Used for smooth transitions between forms.

---

## Tips
- You can edit the HTML to add more fields or change text.
- Change CSS colors and padding to customize the look.
- Use JavaScript to add more interactivity.

---

Happy coding! If you have questions, just ask!
