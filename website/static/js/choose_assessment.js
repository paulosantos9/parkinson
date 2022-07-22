if (document.referrer !==  window.location.href) {
    // If coming from other page, user should be redirected to main
    window.location.replace('/backToMain');
}

function chooseButton(divId) {
    index = divId - 1;
    window.location.replace('/assessment?index=' + index);
}

document.getElementById('back').onclick = function() {
    window.location.replace('/backToMain');
};
