let currentStep=1;
const totalSteps=4;
const steps=document.querySelectorAll(".step");
const nextButton=document.getElementById("next-button");
const progressBar=document.getElementById("progress");

nextButton.addEventListener("click",()=> {
    if(validateStep()) {
        if(currentStep<totalSteps) {
            steps[currentStep-1].style.display="none";
            steps[currentStep].style.display="block";
            currentStep++;
            if(currentStep===totalSteps) {
                nextButton.textContent="Sign Up";
                updateSummary();
            }
            progressBar.style.width=`${(currentStep/totalSteps)*100}%`;
        } else {
            document.getElementById("signup-form").submit();
        }
    }
});

function validateStep() {
    let isValid=true;
    document.querySelectorAll(".error-message").forEach(msg=>msg.remove());
    if(currentStep===1) {
        const name=document.getElementById("name");
        const username=document.getElementById("username");
        if(name.value.trim()==="") {
            showError(name,"Name cannot be empty");
            isValid=false;
        }
        if(username.value.trim()==="") {
            showError(username,"Username cannot be empty");
            isValid=false;
        }
    }
    if(currentStep===2) {
        const email=document.getElementById("email");
        const emailPattern=/^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if(email.value.trim()==="") {
            showError(email,"Email cannot be empty");
            isValid=false;
        } else if(!emailPattern.test(email.value.trim())) {
            showError(email,"Email is not valid");
            isValid=false;
        }
    }
    if(currentStep===3) {
        const password=document.getElementById("password");
        const confirmPassword=document.getElementById("confirm-password");
        if(password.value.trim()==="") {
            showError(password,"Password cannot be empty");
            isValid=false;
        }
        if(confirmPassword.value.trim()==="") {
            showError(confirmPassword,"Confirm Password cannot be empty");
            isValid=false;
        }
        if(password.value!==confirmPassword.value) {
            showError(confirmPassword,"Passwords do not match");
            isValid=false;
        }
    }

    return isValid;
}

function showError(inputElement,message) {
    const errorMessage=document.createElement("div");
    errorMessage.className="error-message";
    errorMessage.style.color="red";
    errorMessage.style.fontSize="12px";
    errorMessage.textContent=message;
    inputElement.style.borderColor="red";
    inputElement.parentElement.insertBefore(errorMessage,inputElement);
}

function updateSummary() {
    document.getElementById("summary-name").textContent=document.getElementById("name").value;
    document.getElementById("summary-username").textContent=document.getElementById("username").value;
    document.getElementById("summary-email").textContent=document.getElementById("email").value;
}
