// Draw
let color = "black";
const strokeSize = 3;

var currTouch = null;
var currTouchInterval = null;

function getOffset(el) {
    const rect = el.getBoundingClientRect();
    return {
      left: rect.left + window.scrollX,
      top: rect.top + window.scrollY
    };
}

function startDraw() {
  const canvas = document.querySelector("#canvas");
  const ctx = canvas.getContext("2d");

  //resizing
  document.getElementById('container').clientHeight > document.getElementById('container').clientWidth ? side = document.getElementById('container').clientWidth*0.9 : side = document.getElementById('container').clientHeight*0.9 - 95;
  canvas.height = side;
  canvas.width = side;
  let marginLeft = Math.floor( (document.getElementById('container').clientWidth - side) / 2) // (100% - 90%) / 2 = 5% margin
  canvas.style.marginLeft = marginLeft.toString() + 'px'; // 5% 90% 5%
  canvas.fillStyle = '#FFF';
  
  //variables
  let painting = false;

  //functions
  function startPosition(e) {
    painting = true;
    draw(e);

    console.log(e.touches);
  }

  function endPosition() {
    painting = false;
    ctx.beginPath();
  }

  function draw(e) {
    if (!painting) {
      return;
    }
    
    e.preventDefault();
    ctx.lineWidth = strokeSize;
    ctx.lineCap = "round";
 
    // ctx.lineTo(e.clientX, e.clientY);
    if (e.type == 'touchmove'){
      ctx.lineTo(e.touches[0].clientX-getOffset(canvas).left, e.touches[0].clientY-getOffset(canvas).top);
    } else if (e.type == 'mousemove'){
      ctx.lineTo(e.clientX-getOffset(canvas).left, e.clientY-getOffset(canvas).top);
    }
      
    ctx.stroke();
    ctx.strokeStyle = color;
    ctx.beginPath();
    
    // ctx.moveTo(e.clientX, e.clientY);
    if (e.type == 'touchmove'){
      ctx.moveTo(e.touches[0].clientX-getOffset(canvas).left, e.touches[0].clientY-getOffset(canvas).top);
    } else if (e.type == 'mousemove'){
      ctx.moveTo(e.clientX-getOffset(canvas).left, e.clientY-getOffset(canvas).top);
    }
  }

  //event listeners
  canvas.addEventListener("mousedown", startPosition);
  canvas.addEventListener("touchstart", startPosition);
  canvas.addEventListener("mouseup", endPosition);
  canvas.addEventListener("touchend", endPosition);
  canvas.addEventListener("mousemove", draw);
  canvas.addEventListener("touchmove", draw);
}

window.onresize = startDraw;

function sendPostWithScore(image) {
  let now = new Date();
  timeSpent = (now.getTime() - starterTimer)/1000;
  let data = {'image': image,'gameType': 4, 'timeSpent': timeSpent};
  fetch("/game", {
      method: "POST",
      headers: {'Content-Type': 'application/json'}, 
      body: JSON.stringify(data)
  }).then(res => {
      window.location.replace('/');
  });
}

function guardar() {
    sendPostWithScore(canvas.toDataURL());
}

document.getElementById('apagar').onclick = startDraw;

document.getElementById('guardar').onclick = guardar;


// Menu inicial
document.getElementById('exit-game').onclick = function() {
    window.location.replace('/backToMain')
}

document.getElementById('start-game').onclick = function() {
    document.getElementById('start-game').style.display = 'none';
    document.getElementById('exit-game').style.display = 'none';
    document.getElementById('container').style.display = 'block';
    let now = new Date();
    starterTimer = now.getTime();
    startDraw();
}