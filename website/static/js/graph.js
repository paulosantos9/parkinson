if (document.referrer !==  window.location.href) {
  // If coming from other page, user should be redirected to main
  window.location.replace('/backToMain');
}

document.getElementById('back').onclick = function() {
  window.location.replace('/choose_evolution');
};

function padTo2Digits(num) {
  return num.toString().padStart(2, "0");
}

function formatDate(date) {
  return (
    [
      date.getFullYear(),
      padTo2Digits(date.getMonth() + 1),
      padTo2Digits(date.getDate()),
    ].join("-") +
    " " +
    [
      padTo2Digits(date.getHours()),
      padTo2Digits(date.getMinutes()),
      padTo2Digits(date.getSeconds()),
    ].join(":")
  );
}

function get_data() {
  fetch("/games_data/" + document.getElementById('index').textContent)
    .then((response) => response.json())
    .then((data) => {
      // adjust data
      let xvalues = [];
      let yvalues_score = [];
      let yvalues_time = [];
      for (var i = 0; i < data.games_list.length; i++) {
        xvalues.push(formatDate(new Date(data.games_list[i].currentTime)));
        yvalues_score.push(data.games_list[i].score);
        yvalues_time.push(data.games_list[i].timeSpent);
      }
      let gameIndex = document.getElementById('index').textContent;
      let dataGraph;
      let layout;
      if (parseInt(gameIndex) === 1 || parseInt(gameIndex) === 2) {
        // reaction, only score
        dataGraph = [
          { // score
            x: xvalues,
            y: yvalues_score,
            type: 'scatter',
            name: 'Score',
          }
        ];
        layout = {
          title: data.type,
          autosize: true,
          margin: {
            l: 50,
            r: 50,
            b: 50,
            t: 50,
            pad: 4
          },
          yaxis: {title: 'Score (' + data.unit + ')'}
        };
      } else if (parseInt(gameIndex) === 3 || parseInt(gameIndex) === 4 || parseInt(gameIndex) === 5) {
        dataGraph = [
          { // score
            x: xvalues,
            y: yvalues_score,
            type: 'scatter',
            name: 'Score',
          },
          { // time
            x: xvalues,
            y: yvalues_time,
            type: 'scatter',
            name: 'Tempo',
            yaxis: 'y2',
          },
        ]
        layout = {
          title: data.type,
          autosize: true,
          margin: {
            l: 50,
            r: 50,
            b: 50,
            t: 50,
            pad: 4
          },
          yaxis: {title: 'Score (' + data.unit + ')'},
          yaxis2: {
            title: 'Tempo (s)',
            titlefont: {color: 'rgb(0, 0, 0)'},
            tickfont: {color: 'rgb(0, 0, 0)'},
            overlaying: 'y',
            side: 'right'
          }
        };
      } else { // Audio
        let jitter_list = [];
        let shimmer_list = [];
        for (var i = 0; i < data.games_list.length; i++) {
          console.log(data.games_list[i].jitter)
          jitter_list.push(parseFloat(data.games_list[i].jitter));
          shimmer_list.push(parseFloat(data.games_list[i].shimmer));
        }
        dataGraph = [
          { // score
            x: xvalues,
            y: jitter_list,
            type: 'scatter',
            name: 'Jitter',
          },
          { // time
            x: xvalues,
            y: shimmer_list,
            type: 'scatter',
            name: 'Shimmer',
            yaxis: 'y2',
          },
        ]
        layout = {
          title: data.type,
          autosize: true,
          margin: {
            l: 50,
            r: 50,
            b: 50,
            t: 50,
            pad: 4
          },
          yaxis: {title: 'Jitter'},
          yaxis2: {
            title: 'Shimmer',
            titlefont: {color: 'rgb(0, 0, 0)'},
            tickfont: {color: 'rgb(0, 0, 0)'},
            overlaying: 'y',
            side: 'right'
          }
        };
      }
      //links = ['google.com/1', 'google.com/2']
      var myPlot = document.getElementById('myChart');
      Plotly.newPlot(myPlot, dataGraph, layout, {displayModeBar: false});
      /*myPlot.on('plotly_click', function(data){
        console.log(data.points[0])
        if (data.points.length === 1) {
          var link = links[data.points[0].pointNumber];
          
          // Note: window navigation here.
          //window.location = link;
        }
      });*/
    });
}

get_data();
