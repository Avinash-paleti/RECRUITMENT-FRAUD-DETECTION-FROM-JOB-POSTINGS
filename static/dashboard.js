async function loadStats(){

let res = await fetch("http://127.0.0.1:5000/stats");

let data = await res.json();

document.getElementById("total").innerText = data.total
document.getElementById("fraud").innerText = data.fraud
document.getElementById("genuine").innerText = data.genuine
document.getElementById("suspicious").innerText = data.suspicious

new Chart(document.getElementById("fraudChart"),{

type:"pie",

data:{
labels:["Fraud","Genuine","Suspicious"],
datasets:[{
data:[
data.fraud,
data.genuine,
data.suspicious
]
}]
}

})

}

loadStats()