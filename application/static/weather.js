$(document).ready(function (){
    function handleWeatherResponse(response, status, xhr){
        console.log(response);

        let forecast = response.query.results.channel.item.forecast;
        $("#weather").empty();

        for (let i of forecast){
            $("#weather").append(i.date + " " + i.day + " " + i.high + " " + i.low + " " + i.text + "<br>");
        };
        renderChart(forecast);
    }

    function weatherButtonClicked(){
        console.log("Please hold while we fetch the forecasts...");

        var url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22Chicago%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
        $.getJSON(url, handleWeatherResponse);
    }

    function renderChart(forecast){

        var highs = []
        var lows = []
        var dates = []
        var days = []
        for (let i of forecast){
            highs.push(parseInt(i.high))
            lows.push(parseInt(i.low))
            dates.push(i.date)
            days.push(i.day)
        }

        console.log(highs);
        console.log(lows.join);
        console.log(dates);
        console.log(days);

        Highcharts.chart('container1', {
            chart: {
                type: 'column'
            },
            title: {
                text: "This Week's Chicago Forecast"
            },
            subtitle: {
                text: 'Source: butaire.com'
            },
            xAxis: {
                categories: dates
            },
            yAxis: {
                title: {
                    text: 'Temperature in Farenheit'
                }
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: true
                }
            },
            series: [{
                name: 'Highs',
                data: highs,
                color: '#f28f43'
            }, {
                name: 'Lows',
                data: lows,
                color: '#2f7ed8'
            }]
        });
    };

    $("#getForecast").click(weatherButtonClicked);
})