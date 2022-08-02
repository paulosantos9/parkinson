document.getElementById('back').onclick = function() {
    window.location.replace('/choose_assessment_list');
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
    fetch("/assessments_data")
      .then((response) => response.json())
      .then((data) => {
        // adjust data
        let xvalues = [];
        let symptoms = [];
        let medications = [];
        for (var i = 0; i < data.assessments_list.length; i++) {
          xvalues.push(formatDate(new Date(data.assessments_list[i].time)));
          symptoms.push(data.assessments_list[i].answer);
        }
        for (var i = 0; i < data.medication_list.length; i++) {
          medications.push({
            type: 'line',
            x0: formatDate(new Date(data.medication_list[i])),
            x1: formatDate(new Date(data.medication_list[i])),
            y0: -1,
            y1: 2,
            line: {
              color: 'red',
              width: 2,
            },
          })          
        }
        // horizontal line
        medications.push({
          type: 'line',
          x0: new Date(2020, 1, 1, 0, 0, 0, 0),
          x1: new Date(2030, 1, 1, 0, 0, 0, 0),
          y0: 1,
          y1: 1,
          line: {
            color: 'black',
            width: 1,
            dash: 'dot'
          }
        })

        dataGraph = [
            { // score
              x: xvalues,
              y: symptoms,
              type: 'scatter',
              name: 'Variações',
              line: {
                color: 'rgb(55, 128, 191)',
                width: 5
              }
            }
        ];
        const dayStart = document.getElementById('day-start').value;
        const dayEnd = document.getElementById('day-end').value;
        let startDay, endDay;
        if (dayStart && dayEnd) {
          startDay = new Date(dayStart.split('-')[0], parseInt(dayStart.split('-')[1])-1, dayStart.split('-')[2], 6, 0, 0, 0);
          endDay = new Date(dayEnd.split('-')[0], parseInt(dayEnd.split('-')[1])-1, dayEnd.split('-')[2], 23, 59, 59, 0);          
        } else {
          const currentDay = new Date();
          startDay = new Date(currentDay.getFullYear(), currentDay.getMonth(), currentDay.getDate(), 6, 0, 0, 0);
          endDay = new Date(currentDay.getFullYear(), currentDay.getMonth(), currentDay.getDate()+1, 0, 0, 0, 0);    
        }

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
            xaxis: {
                range: [formatDate(startDay), formatDate(endDay)]
            },
            yaxis: {
                title: 'Variação',
                range: [0, 1]
            },
            shapes: medications
        };

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
  
document.getElementById('day-start').addEventListener('change', (event) => {
  get_data();
});

document.getElementById('day-end').addEventListener('change', (event) => {
  get_data();
});