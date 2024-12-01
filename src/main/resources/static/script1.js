function getRec() {
    // Send data to the backend
    console.time("timer1");
    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then(response => response.json())
        .then(data => {
            document.getElementsByTagName("h1")[0].innerHTML = "Ваш рекомендованный способ: " + data["class"]
            console.log(data)
            console.timeEnd("timer1");
        })
        .catch(error => {
            console.error('Error:', error);
        });
}