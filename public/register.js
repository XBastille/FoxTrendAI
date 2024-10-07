let currentStep = 1;
const totalSteps = 4;
const steps = document.querySelectorAll(".step");
const nextButton = document.getElementById("next-button");
const progressBar = document.getElementById("progress");
const back = document.getElementById('back')

back.addEventListener('click', () => {
    if (currentStep > 1) {
        steps[currentStep - 1].style.display = "none";
        steps[currentStep - 2].style.display = "block";
        currentStep--;
        backss();
        handleback();
        submitdataback()
        progressBar.style.width = `${(currentStep / totalSteps) * 100}%`;
    }
})

async function handleback() {
    try {
        const response = await fetch('/user/register', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json'
            },
            body: JSON.stringify({img:counts.img})
        })
        const datas = await response.json()
        console.log(datas)
    } catch (error) {
        console.log(error)
    }
}

function submitdataback() {
    fetch('/user/register', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify({img:counts.img}),

    })
        .then((res) => res.json())
        .then(data => {
            console.log(data)
        })
        .catch(err => console.log(err))
}

let counts={
    img:0
}


let formdata = {
    name: "",
    username: "",
    email: "",
    password: "",
    password2: ""
}

const userexist = "User exists"
const userregistered = 'User registered sucessfully'

async function handle() {
    try {
        const response = await fetch('/user/register', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json'
            },
            body: JSON.stringify({...formdata,img:counts.img})
        })
        const datas = await response.json()
        if (datas.sucess === 'false') {
            return userexist;
        }
        if (datas.sucess === 'true') {
            return userregistered
        }
    } catch (error) {
        console.log(error)
    }
}


function submitdata() {
    fetch('/user/register', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify({...formdata,img:counts.img}),

    })
        .then((res) => res.json())
        .then(data => {
            console.log(data)
        })
        .catch(err => console.log(err))
}

nextButton.addEventListener("click", async () => {
    formdatas();
    
    console.log(formdata);
    let result;
    if (currentStep === 1) {
        result = await handle();
        if (result === 'User exists') {
            const usernamess = document.getElementById("username");
            showErrors(usernamess, "Username already exists");
            currentStep = 1;
            counts.img = 0;
            return;
        }
    }
    if (currentStep === 2) {
        result = await handle();
        if (result === 'User exists') {
            const emailss = document.getElementById("email");
            showErrors(emailss, "Email already exists");
            currentStep = 2;
            counts.img = 1;
            progressBar.style.background = "red";
            return;
        }
    }

    if (validateStep()) {
        if (currentStep < totalSteps) {
            steps[currentStep - 1].style.display = "none";
            steps[currentStep].style.display = "block";
            currentStep++;
            counts.img++;
            progressBar.style.background = "white";

            if (currentStep === totalSteps) {
                counts.img = 3;
                nextButton.textContent = "Sign Up";
                updateSummary();
            }

            progressBar.style.width = `${(currentStep / totalSteps) * 100}%`;
            
        } else if (currentStep === totalSteps) {
            counts.img = 3;
            submitdata();  
            window.location.href = '/user/login';  
        }
    }
});


function validateStep() {
    let isValid = true;
    document.querySelectorAll(".error-message").forEach(msg => msg.remove());
    if (currentStep === 1) {
        const name = document.getElementById("name");
        const username = document.getElementById("username");
        if (name.value.trim() === "") {
            showError(name, "Name cannot be empty");
            isValid = false;
        }
        if (username.value.trim() === "") {
            showError(username, "Username cannot be empty");
            isValid = false;
        }
        submitdata();
    }
    if (currentStep === 2) {
        const email = document.getElementById("email");
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (email.value.trim() === "") {
            showError(email, "Email cannot be empty");
            isValid = false;
        } else if (!emailPattern.test(email.value.trim())) {
            showError(email, "Email is not valid");
            isValid = false;
        }
        submitdata();
    }
    if (currentStep === 3) {
        const password = document.getElementById("password");
        const confirmPassword = document.getElementById("confirm-password");
        if (password.value.trim() === "") {
            showError(password, "Password cannot be empty");
            isValid = false;
            progressBar.style.background = "red"
        }
        if (confirmPassword.value.trim() === "") {
            showError(confirmPassword, "Confirm Password cannot be empty");
            isValid = false;
            progressBar.style.background = "red"
        }
        if (password.value !== confirmPassword.value) {
            showError(confirmPassword, "Passwords do not match");
            isValid = false;
            progressBar.style.background = "red"
        }
        submitdata();
    }

    return isValid;
}

function showError(inputElement, message) {
    const errorMessage = document.createElement("div");
    errorMessage.className = "error-message";
    errorMessage.style.color = "red";
    errorMessage.style.fontSize = "12px";
    errorMessage.textContent = message;
    inputElement.style.borderColor = "red";
    inputElement.parentElement.insertBefore(errorMessage, inputElement);
}

function showErrors(inputElement, message) {
    const errorMessage = document.createElement("div");
    errorMessage.className = "error-message";
    errorMessage.style.color = "red";
    errorMessage.style.fontSize = "12px";
    errorMessage.textContent = message;
    inputElement.style.borderColor = "red";
    inputElement.parentElement.insertBefore(errorMessage, inputElement);
}

function backss(){
    if(currentStep===1){
        counts.img=0;
    }
    if(currentStep ===2){
        counts.img=1;
    }
}

function formdatas() {
    if (currentStep === 1) {
        formdata.name = document.getElementById("name").value.trim();
        formdata.username = document.getElementById("username").value.trim()
    }
    if (currentStep === 2) {
        formdata.email = document.getElementById('email').value.trim()
    }
    if (currentStep === 3) {
        formdata.password = document.getElementById('password').value.trim()
        formdata.password2 = document.getElementById('confirm-password').value.trim();
    }

}

function updateSummary() {
    document.getElementById("summary-name").textContent = document.getElementById("name").value;
    document.getElementById("summary-username").textContent = document.getElementById("username").value;
    document.getElementById("summary-email").textContent = document.getElementById("email").value;
}