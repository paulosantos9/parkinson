
document.getElementById('back').onclick = function() {
    window.location.replace('/info_choose');
};

function changeDisplay(divId) {
    document.getElementById(divId).className === 'question-data' ? document.getElementById(divId).classList.add("show-data") : document.getElementById(divId).classList.remove("show-data");
}