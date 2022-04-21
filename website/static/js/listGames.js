function cookieToJson() {
    var cookie = document.cookie;
    var output = {};
    cookie.split(/\s*;\s*/).forEach(function(pair) {
      pair = pair.split(/\s*=\s*/);
      output[pair[0]] = pair.splice(1).join('=');
    });
    return output;
}

let gameScores = cookieToJson();

for (var key in gameScores){
  var value = gameScores[key];
  var newScore = document.createElement('button');
  newScore.className = 'btn scoreDiv';
  newScore.id = key;
  document.getElementsByClassName('signin-signup')[0].appendChild(newScore);
  console.log(key);
  document.getElementById(key).textContent = 'Score: ' + value;
}
