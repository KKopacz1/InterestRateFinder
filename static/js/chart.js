google.charts.load('current', {'packages':['gauge']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {

  var data = google.visualization.arrayToDataTable([
    ['Label', 'Value'],
    /* Add the Script value here - Might need a new route on app.py */
    ['Rate', 37],
  ]);

  var options = {
    width: 600, height: 540,
    redFrom: 27, redTo: 50,
    yellowFrom:13, yellowTo: 27,
    greenFrom: 0, greenTo: 13,
    min: 0, max: 50,
    minorTicks: 0, majorTicks: 4
  };

  var chart = new google.visualization.Gauge(document.getElementById('chart_div'));

  chart.draw(data, options);
};