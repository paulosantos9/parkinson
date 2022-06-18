document.getElementById('games').onclick = function() {
    if( ('ontouchstart' in document.documentElement && /mobi/i.test(navigator.userAgent)) ) {
        // if is mobile
        window.location.replace('/game');
    } else {
        // não pode jogar equilibrio
        window.location.replace('/game/pc');
    }
};

document.getElementById('assessment').onclick = function() {
    window.location.replace('/choose_assessment');
};

document.getElementById('account').onclick = function() {
    window.location.replace('/account');
};

document.getElementById('logout').onclick = function() {
    window.location.replace('/logout');
};
