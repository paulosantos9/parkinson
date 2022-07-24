
function chooseButton(id) {
    window.location.replace('/choose_assessment/' + id);
}

document.getElementById('back').onclick = function() {
    window.location.replace('/account_options');
};
