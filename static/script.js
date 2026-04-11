document.getElementById("loginForm").addEventListener("submit", function(e){

e.preventDefault();

let username = document.getElementById("username").value;
let password = document.getElementById("password").value;

if(username === "admin" && password === "1234"){
document.getElementById("message").innerText = "Login Successful";
}
else{
document.getElementById("message").innerText = "Invalid Credentials";
}

});