function showPassword() {
    var input = document.getElementById("password");
    var button = document.getElementById("password-button");
    if (input.type === "password") {
        input.type = "text";
        button.classList.add('btn-password-hide');
    } else {
        input.type = "password";
        button.classList.remove('btn-password-hide');
    }
}

function showPassword2() {
    var input = document.getElementById("password2");
    var button = document.getElementById("password2-button");
    if (input.type === "password") {
        input.type = "text";
        button.classList.add('btn-password-hide');
    } else {
        input.type = "password";
        button.classList.remove('btn-password-hide');
    }
}
function validatePassword() {
    var password = document.getElementById("password");
    var password2 = document.getElementById("password2");
    if (password.value == password2.value) {
        password2.setCustomValidity("");
    } else {
        password2.setCustomValidity("Las contraseñas no coinciden");
    }
}