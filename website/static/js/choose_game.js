document.getElementById('random').onclick = function() {
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

document.getElementById('reacao').onclick = function() {
    window.location.replace('/game/1');
};

document.getElementById('rapidez').onclick = function() {
    window.location.replace('/game/2');
};

document.getElementById('memoria').onclick = function() {
    window.location.replace('/game/3');
};

document.getElementById('desenho').onclick = function() {
    window.location.replace('/game/4');
};

document.getElementById('equilibrio').onclick = function() {
    window.location.replace('/game/5');
};

document.getElementById('falar').onclick = function() {
    window.location.replace('/game/6');
};

document.getElementById('voltar').onclick = function() {
    window.location.replace('/');
};
