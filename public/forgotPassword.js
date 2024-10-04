function showError(inputElement, message) {
    const errorMessage = document.createElement("div");
    errorMessage.className = "error-message";
    errorMessage.style.color = "red";
    errorMessage.style.fontSize = "12px";
    errorMessage.textContent = message;
    inputElement.style.borderColor = "red";
    inputElement.parentElement.insertBefore(errorMessage, inputElement);
}