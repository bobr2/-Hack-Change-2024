// data.js

// Пример данных о способах оплаты в формате JSON
const paymentMethods = {
    method: "токен"
};

// Функция для получения способа оплаты
function getPaymentMethod() {
    return paymentMethods.method;
}

function getRec() {
    // Send data to the backend
    console.time("timer1");
    return fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then(response => response.json())
        .then(data => {
            console.log(data["class"]);
            console.timeEnd("timer1");
            return data["class"];
        })
        .catch(error => {
            console.error('Error:', error);
        });
}