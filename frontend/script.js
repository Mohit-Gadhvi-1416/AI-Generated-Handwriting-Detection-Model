document.getElementById('uploadForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData();
    const pdfFile = document.getElementById('pdfFile').files[0];
    formData.append('pdf', pdfFile);

    fetch('http://localhost:3000/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = '<h2>Results</h2>';
        if (data.error) {
            resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
        } else {
            resultDiv.innerHTML += `<p>Prediction: ${data.prediction}</p>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing the file.');
    });
});
