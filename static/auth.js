const API = "http://127.0.0.1:5000";

async function register() {

const name = document.getElementById("name").value;
const email = document.getElementById("email").value;
const password = document.getElementById("password").value;
const role = document.getElementById("role").value;

const res = await fetch(API + "/register", {
method: "POST",
headers: {
"Content-Type": "application/json"
},
body: JSON.stringify({
name: name,
email: email,
password: password,
role: role
})
});

const data = await res.json();

if(data.status === "success"){
alert("Registration successful!");
window.location.href = "login.html";
}else{
alert(data.message);
}

}

async function login(){

const email = document.getElementById("email").value;
const password = document.getElementById("password").value;

const res = await fetch(API + "/login",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
email:email,
password:password
})
});

const data = await res.json();

if(data.status === "success"){

localStorage.setItem("token",data.token);
localStorage.setItem("role",data.role);

if(data.role === "admin"){
window.location.href="admin.html";
}else{
window.location.href="scan.html";
}

}else{
alert("Invalid login credentials");
}

}