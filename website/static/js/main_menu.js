document.getElementById('sente').onclick = function() {
    window.location.replace('/assessment?index=0');
};

document.getElementById('games').onclick = function() {
    window.location.replace('/choose_game');
};

document.getElementById('assessment').onclick = function() {
    window.location.replace('/choose_assessment');
};

document.getElementById('info').onclick = function() {
    window.location.replace('/info');
};

document.getElementById('account').onclick = function() {
    window.location.replace('/account_options');
};

document.getElementById('logout').onclick = function() {
    window.location.replace('/logout');
};
