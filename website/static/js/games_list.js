if (document.referrer !==  window.location.href) {
  // If coming from other page, user should be redirected to main
  window.location.replace('/backToMain');
}

document.getElementById('back').onclick = function() {
  window.location.replace('/account');
};

function changeDisplay(divId) {
  document.getElementById(divId).className === 'game-data-inner' ? document.getElementById(divId).classList.add("show-data") : document.getElementById(divId).classList.remove("show-data");
  document.getElementById(divId+'-title').className === 'align-center' ? document.getElementById(divId+'-title').classList.add("hide-data") : document.getElementById(divId+'-title').classList.remove("hide-data");
}