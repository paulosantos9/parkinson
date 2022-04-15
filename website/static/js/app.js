const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});

function handleNotifications() {
  // Let's check if the browser supports notifications
  if (!("Notification" in window)) {
    alert("Cuidado, este navegador não suporta notificações !");
  }
  
  // Let's check whether notification permissions have already been granted
  else if (Notification.permission === "granted") {
    // If it's okay let's create a notification
    var notification = new Notification("Hi there!");
    notification.onclick = function(event) {
      event.preventDefault(); // prevent the browser from focusing the Notification's tab
      window.location.replace('/login')
    }
  }

  else {
    Notification.requestPermission('As notificações são importantes').then(function (permission) {
      // If the user accepts, let's create a notification
      if (permission === "granted") {
        var notification = new Notification("Hi there!");
        notification.onclick = function(event) {
          //event.preventDefault(); // prevent the browser from focusing the Notification's tab
          window.location.replace('/login')
        }
      }
    });
  }
}

function printMinutes() {
  now = new Date();
  currentMinute = parseInt(now.getMinutes())
  if (currentMinute == 6 || currentMinute == 7 || currentMinute == 8 || currentMinute == 9 || currentMinute == 10 || currentMinute == 11) // every hour
    handleNotifications()
}
setInterval(printMinutes, 60000);