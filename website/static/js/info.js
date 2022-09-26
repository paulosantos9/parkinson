
document.getElementById('back').onclick = function() {
    window.location.replace('/');
};

function changeDisplay(divId) {
    document.getElementById(divId).className === 'question-data' ? document.getElementById(divId).classList.add("show-data") : document.getElementById(divId).classList.remove("show-data");
}