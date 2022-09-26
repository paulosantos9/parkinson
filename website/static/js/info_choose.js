
function chooseButton(divId) {
    index = divId - 1;
    window.location.replace('/info');
}

document.getElementById('back').onclick = function() {
    window.location.replace('/');
};
