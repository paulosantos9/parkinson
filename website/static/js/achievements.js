if (document.referrer !==  window.location.href) {
    // If coming from other page, user should be redirected to main
    window.location.replace('/backToMain');
}

document.getElementById('back').onclick = function() {
    window.location.replace('/account');
};