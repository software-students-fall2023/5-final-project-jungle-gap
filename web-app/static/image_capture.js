// Grab elements, create settings, etc.
var count = 0; // if ever clicked taking a photo
var video = document.getElementById("video");
// Elements for taking the snapshot
var canvas = document.getElementById("canvas");
var context = canvas.getContext("2d");

var toShoot = document.getElementById("to-shoot");
var savePhoto = document.getElementById("save-photo");

var uploadForm = document.getElementById("upload-form");

var imageFile = document.getElementById("image-file");

uploadForm.addEventListener("submit", async function (event) {
  event.preventDefault(); // Prevent the normal submission of the form

  // Display a processing message
  document.getElementById("response-message").innerHTML =
    "<p class='processing-status'>Processing image file...</p>";

  console.log("uploadForm.addEventListener this=", this);

  let formData = new FormData(this); // 'this' refers to the form

  let response = await fetch("/api/upload_image", {
    method: "POST",
    body: formData,
  });
  let blob = await response.blob();

  updateResultPage(blob); // Use the same function to update the page
});

toShoot.addEventListener("click", async () => {
  console.log("Start to-shoot button clicked");

  // Get access to the camera!
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Not adding `{ video: true }` since we only want video now
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then(function (stream) {
        //video.src = window.URL.createObjectURL(stream);
        video.srcObject = stream;
        video.play();
      });
  }

  context.drawImage(video, 0, 0, 300, 180);
  count++;
  if (video.paused) {
    toShoot.innerText = "take a picture";
    video.play();
  } else {
    toShoot.innerText = "take again";
    video.pause();
  }

  // Update UI to show processing status
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
  console.log("Stop recording button clicked");

  if (count === 0) {
    alert("take a picture first");
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
  console.log("Sending image to server");
  const formData = new FormData();
  formData.append("image", imgBlob, "test.png");

  fetch("/api/js_upload_image", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      console.log("response===", response.arrayBuffer);

      if (!response.ok) {
        throw new Error("Network response was not ok: " + response.statusText);
      } else {
        console.log("Upload successful", response);
        let blob = new Blob([response.body], {
          type: "image/png",
        });

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

  let htmlContent = `
        <div>
            <h3>Result:</h3>
        </div>
    `;

  resultContainer.innerHTML = htmlContent;
  resultContainer.append(img);
}

imageFile.addEventListener("change", function () {
  var fileName = this.files[0].name;
  document.getElementById("file-chosen").textContent = fileName; // Updates the span text
});
