if (document.referrer !==  window.location.href) {
    // If coming from other page, user should be redirected to main
    window.location.replace('/backToMain');
}

document.getElementById('results').onclick = function() {
    window.location.replace('/choose_evolution');
};

document.getElementById('assessments').onclick = function() {
    window.location.replace('/assessments');
};

document.getElementById('achievements').onclick = function() {
    window.location.replace('/achievements');
};

document.getElementById('back').onclick = function() {
    window.location.replace('/backToMain');
};
