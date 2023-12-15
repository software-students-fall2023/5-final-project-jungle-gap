// Grab elements, create settings, etc.
var count = 0; // if ever clicked taking a photo
var video = document.getElementById("video");

// Elements for taking the snapshot
var canvas = document.getElementById("canvas");
var context = canvas.getContext("2d");

var toShoot = document.getElementById("to-shoot");
var savePhoto = document.getElementById("save-photo");

// Initially disable the recognize (savePhoto) button
savePhoto.disabled = true;

var uploadForm = document.getElementById("upload-form");
var imageFile = document.getElementById("image-file");
var responseMessage = document.getElementById("response-message");

uploadForm.addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent the normal submission of the form

  // Clear any previous response messages
  responseMessage.innerHTML = "";

  // Check if an image is selected
  if (imageFile.files.length === 0) {
      responseMessage.innerHTML = "<p class='error-status'>Please select an image file to upload.</p>";
      return;
  }

  // Check if the file is an image
  const imageFileSelected = imageFile.files[0];
  if (!imageFileSelected.type.startsWith('image/')) {
      responseMessage.innerHTML = "<p class='error-status'>Please select a valid image file.</p>";
      return;
  }

  // Display a processing message
  responseMessage.innerHTML = "<p class='processing-status'>Processing image file...</p>";

  let formData = new FormData(this); // 'this' refers to the form

  fetch('/api/upload_image', {
      method: 'POST',
      body: formData,
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.blob();
  })
  .then(blob => {
      updateResultPage(blob); // Use the same function to update the page
  })
  .catch(error => {
      console.error('Error uploading file:', error);
      responseMessage.innerHTML = "<p class='error-status'>Error uploading file, please try again!</p>";
  });
});

toShoot.addEventListener("click", async () => {
  // Get access to the camera!
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then(function (stream) {
        video.srcObject = stream;
        video.play();
      });
  }

  if (!video.paused) {
    context.drawImage(video, 0, 0, 300, 180);
    count++;
    toShoot.innerText = "Take Again";
    video.pause();

    // Enable the recognize (savePhoto) button after taking a photo
    savePhoto.disabled = false;
  } else {
    video.play();
    toShoot.innerText = "Take a Photo";
    savePhoto.disabled = true; // Disable recognize button if not ready to take a photo
  }

  document.getElementById("response-message").innerHTML =
    "<p class='processing-status'>Loading...</p>";
});

function b64toBlob(dataURI) {
  var byteString = atob(dataURI.split(",")[1]);
  var ab = new ArrayBuffer(byteString.length);
  var ia = new Uint8Array(ab);
  for (var i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
  }
  return new Blob([ab], { type: "image/png" });
}

savePhoto.addEventListener("click", async () => {
  if (count === 0) {
    alert("Please take a picture first");
  } else {
    let blob = await new Promise((resolve) =>
      canvas.toBlob(resolve, "image/png")
    );
    document.getElementById("response-message").innerHTML =
      "<p class='processing-status'>Processing ...</p>";
    sendImageToServer(blob);
  }
});

function sendImageToServer(imgBlob) {
  const formData = new FormData();
  formData.append("image", imgBlob, "test.png");
  fetch("/api/js_upload_image", {
    method: "POST",
    body: formData,
  })
    .then(async (response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok: " + response.statusText);
      } else {
        let blob = await response.blob();
        updateResultPage(blob);
      }
    })
    .catch((error) => {
      console.error("Error uploading image:", error);
    });
}

function updateResultPage(blob) {
  let resultContainer = document.getElementById("response-message");
  let img = document.createElement("img");
  img.src = URL.createObjectURL(blob);
  let htmlContent = "<div><h3>Result:</h3></div>";
  resultContainer.innerHTML = htmlContent;
  resultContainer.append(img);
}

imageFile.addEventListener("change", function () {
  var fileName = this.files[0].name;
  document.getElementById("file-chosen").textContent = fileName;
});
