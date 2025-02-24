function uploadVideo() {
    let fileInput = document.getElementById('videoUpload');
    let file = fileInput.files[0];

    if (!file) {
        alert("Please select a video file.");
        return;
    }

    let formData = new FormData();
    formData.append("video", file);

    fetch("https://your-backend-api.com/predict", {  // Replace with your backend URL
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = "Predicted Action: " + data.action;
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("result").innerText = "Error in prediction.";
    });
}
