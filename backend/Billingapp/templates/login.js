// Code for toggling password visibility
const passwordInputs = document.querySelectorAll("input[type=password]");
for (let input of passwordInputs) {
  const toggleButton = document.createElement("button");
  toggleButton.textContent = "Show";
  toggleButton.classList.add("password-toggle");
  toggleButton.addEventListener("click", () => {
    if (input.type === "password") {
      input.type = "text";
      toggleButton.textContent = "Hide";
    } else {
      input.type = "password";
      toggleButton.textContent = "Show";
    }
  });
  input.parentNode.appendChild(toggleButton);
}
