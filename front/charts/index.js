import Chart from 'chart.js';
var ctx = document.getElementById("myChart");



function calculateNewGraph(i) {
    let historicalData = dataset[i].historical;
    let predictedData = dataset[i].predicted;
    let actualData = dataset[i].actual;

    var historicalTimeSeries = [];

    var historicalWeatherSeries = [];
    var predictedWeatherSeries = [];
    var actualWeatherSeries = [];
    console.log("before historicalTimeSeries: " + historicalTimeSeries);
    for (let key in historicalData) {
        let time = historicalData[key].time;
        historicalTimeSeries.push(time);
        let rain = historicalData[key].rain;
        historicalWeatherSeries.push(rain);
        predictedWeatherSeries.push(0);
        actualWeatherSeries.push(0);
    }
    console.log("after first loop: " + historicalTimeSeries.length);

    for (let key in predictedData) {
        let time = predictedData[key].time;
        historicalTimeSeries.push(time);
        let rain = predictedData[key].rain;
        predictedWeatherSeries.push(rain);
    }
    console.log("after 2nd loop: " + historicalTimeSeries.length);

    for (let key in actualData) {
        let rain = actualData[key].rain;
        actualWeatherSeries.push(rain);
    }
    console.log("after 3rd loop: " + historicalTimeSeries.length);

    let myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: historicalTimeSeries,
            datasets: [{
                    borderWidth: 3,
                    borderColor: "rgba(0,0,0,0.5)", // and not lineWidth,
                    data: historicalWeatherSeries,
                    label: "Historical Data",
                    backgroundColor: "rgba(153,255,51,0.4)"
                },
                {
                    borderWidth: 3, // and not lineWidth,
                    borderColor: "rgba(0,0,0,0.5)", // and not lineWidth,
                    data: predictedWeatherSeries,
                    label: "Predicted Data",
                    backgroundColor: "rgba(255,153,0,0.4)"
                },
                {
                    borderWidth: 3, // and not lineWidth,
                    borderColor: "rgba(0,0,0,0.5)", // and not lineWidth,
                    data: actualWeatherSeries,
                    label: "Actual Data",
                    backgroundColor: "rgba(0,153,0,0.4)"
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }],
                xAxes: [{
                    type: 'time',
                    time: {}
                }]
            }
        }
    });
}
let dataset = require('./dataset');
var i = 1;
calculateNewGraph(i);
document.getElementById("next-iteration").addEventListener("click", function () {
    if (i < 10) {
        calculateNewGraph(i);
        i++;
    } else {
        console.log("last iteration reached");
    }
});