var timer;
let minute = 0;
let second = 0;

setTimeout(function () {
  timer = document.getElementById("timer");
}, 100);

setTimeout(function () {
  minute = Number(timer.innerText.split(":")[0]);
  second = Number(timer.innerText.split(":")[1]);
}, 200);

setInterval(function () {
  second--;
  if (second < 0) {
    second = 59;
    minute--;
  }
  if (minute < 0) {
    minute = 0;
    second = 0;
  }

  if (minute === 0 && second === 0) {
    setTimeout(function () {
      window.location.reload();
    }, 10000);
  }

  minute = String(minute).padStart(2, "0");
  second = String(second).padStart(2, "0");
  timer.innerText = minute + ":" + second;
}, 1000);
