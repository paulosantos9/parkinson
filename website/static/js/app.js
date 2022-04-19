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
  var options = {
    badge: '/static/images/elder2.png',
    icon: '/static/images/elder2.png',
    vibrate: [200, 100, 200]
  }
  if (!("Notification" in window)) {
    alert("Cuidado, este navegador não suporta notificações !");
  }
  
  // Let's check whether notification permissions have already been granted
  else if (Notification.permission === "granted") {
    // If it's okay let's create a notification
    var notification = new Notification("HORA DO QUIZ !", options);
    notification.onclick = function(event) {
      event.preventDefault(); // prevent the browser from focusing the Notification's tab
      window.location.replace('/login')
    }
  }

  else {
    Notification.requestPermission().then(function (permission) {
      // If the user accepts, let's create a notification
      if (permission === "granted") {
        var notification = new Notification("HORA DO QUIZ !", options);
        notification.onclick = function(event) {
          //event.preventDefault(); // prevent the browser from focusing the Notification's tab
          window.location.replace('/login')
        }
      } else { // Try last time
        Notification.requestPermission().then(function (permission) {
          // If the user accepts, let's create a notification
          if (permission === "granted") {
            var notification = new Notification("HORA DO QUIZ !", options);
            notification.onclick = function(event) {
              //event.preventDefault(); // prevent the browser from focusing the Notification's tab
              window.location.replace('/login')
            }
          }
        });
      }
    });
  }
}

function manageMinutes() {
  now = new Date();
  currentMinute = now.getMinutes();
  currentHour = now.getHours();
  hoursForNotifications = [9, 1, 18, 22]; // ir buscar aos dados do paciente
  // Questionar sobre as melhores horas para fazer os questionários
  // Atualmente verifica se são 9h00, 14h00, 18h00, 22h00
  //if (currentMinute === 0) { // every hour
  if (currentMinute > 0) { // every hour
    if (hoursForNotifications.includes(currentHour))
      handleNotifications()
  }
}

function availableInstantNotification() {
  manageMinutes()
  setInterval(manageMinutes, 60000); // check every minute
}

availableInstantNotification();