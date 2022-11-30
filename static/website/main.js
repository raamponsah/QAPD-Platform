const playStudentVideo = document.getElementById('play-student-video');
const dialog = document.querySelector('#videoDialog');
// const video = document.querySelector("#video")
const close = document.querySelector("#close")
consol.log(close)
playStudentVideo.addEventListener('click', () => {
    if (typeof dialog.showModal === "function") {
        dialog.showModal();
        // video.play();
        console.log('showing dialog');
      } else {
        console.log("Sorry, the <dialog> API is not supported by this browser.");
      }

});

close.addEventListener('click', () => {
    if (typeof dialog.close === "function") {
        dialog.close();
        // video.pause();
        console.log('closing dialog');
        } else {
        console.log("Sorry, the <dialog> API is not supported by this browser.");
        }
});