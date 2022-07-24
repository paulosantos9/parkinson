document.getElementById('sente').onclick = function() {
    window.location.replace('/assessment?index=0');
};

document.getElementById('games').onclick = function() {
    if( ('ontouchstart' in document.documentElement && /mobi/i.test(navigator.userAgent)) ) {
        // if is mobile
        options = [1, 2, 3, 4, 5, 6]
        game = options[Math.floor(Math.random() * options.length)]
        window.location.replace('/game/' + game);
    } else {
        options = [1, 2, 3, 4, 6]
        game = options[Math.floor(Math.random() * options.length)]
        // não pode jogar equilibrio
        window.location.replace('/game/' + game);
    }
};

document.getElementById('assessment').onclick = function() {
    window.location.replace('/choose_assessment');
};

document.getElementById('info').onclick = function() {
    window.location.replace('/info_choose');
};

document.getElementById('account').onclick = function() {
    window.location.replace('/account_options');
};

document.getElementById('logout').onclick = function() {
    window.location.replace('/logout');
};
