if (document.referrer !==  window.location.href) {
    // If coming from other page, user should be redirected to main
    window.location.replace('/backToMain');
}

function chooseButton(id) {
    window.location.replace('/evolution/' + id);
}

document.getElementById('back').onclick = function() {
    window.location.replace('/account');
};
