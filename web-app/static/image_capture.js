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

uploadForm.addEventListener("submit", async function (event) {
  event.preventDefault(); // Prevent the normal submission of the form

  // Display a processing message
  document.getElementById("response-message").innerHTML =
    "<p class='processing-status'>Processing...</p>";

  let formData = new FormData(this); // 'this' refers to the form

  let response = await fetch("/api/upload_image", {
    method: "POST",
    body: formData,
  });
  let blob = await response.blob();

  updateResultPage(blob); // Use the same function to update the page
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
  img.style = "width:200px";
  img.src = URL.createObjectURL(blob);
  let htmlContent = "<div><h3>Result:</h3></div>";
  resultContainer.innerHTML = htmlContent;
  resultContainer.append(img);
}

imageFile.addEventListener("change", function () {
  var fileName = this.files[0].name;
  document.getElementById("file-chosen").textContent = fileName;
});
