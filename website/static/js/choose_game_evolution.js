
function chooseButton(id) {
    window.location.replace('/evolution/' + id);
}

document.getElementById('back').onclick = function() {
    window.location.replace('/account_options');
};
