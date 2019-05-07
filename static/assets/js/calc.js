ENDPOINT = 'localhost:5000';

function calc() {
    const newCapacity = document.getElementById("myRange").value;
    console.log(ENDPOINT + "/calc?capacity=" + newCapacity);
    const Http = new XMLHttpRequest();
    const url= "/calc?capacity=" + newCapacity;
    Http.open("GET", url);
    Http.send();

}