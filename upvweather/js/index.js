function makeRequest(method, url, body, callback, async) {
    if (!async){
        async = true;
    }
    // Obtener la instancia del objeto XMLHttpRequest
    var peticion_http;
    if (window.XMLHttpRequest) {
        peticion_http = new XMLHttpRequest();
    } else if (window.ActiveXObject) {
        peticion_http = new ActiveXObject("Microsoft.XMLHTTP");
    }

    // Preparar la funcion de respuesta
    peticion_http.onreadystatechange = function () {
        if (this.readyState == 4) {
            if (this.status == 200) {
                callback(this.responseText);
            }else{
                alert("Status error: " + this.status)
            }
        }
    }

    // Realizar peticion HTTP
    peticion_http.open(method, url, async);
    peticion_http.send(body);
}
var public_key = 'dZaoR0p6pasmppMl5KRd';
var temperatura = 0.0;
var data2 = [{temp: 4},{temp: 55}];
var graficos = {Gauge: {}, LineChart: {}};
function drawChart() {

    //var data = google.visualization.arrayToDataTable([
    graficos.Gauge.data = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['Temp', temperatura],
        ]);

    graficos.Gauge.options = {
      width: 400, height: 120,
      redFrom: 44, redTo: 50,
      yellowFrom:35, yellowTo: 44,
      minorTicks: 5,
        max: 50,
        min: -10,
        greenColor: "#0EAFFF",
        greenFrom:-10, greenTo: -1
    };

    //var chart = new google.visualization.Gauge(document.getElementById('chart_div'));
    graficos.Gauge.chart = new google.visualization.Gauge(document.getElementById('chart_div'));

    graficos.Gauge.chart.draw(graficos.Gauge.data, graficos.Gauge.options);
    var arr = [];
    graficos.LineChart.data = new google.visualization.DataTable();
    graficos.LineChart.data.addColumn('date', 'X');
    graficos.LineChart.data.addColumn('number', 'Temp');
    graficos.LineChart.data.addRows(arr);
    var options = {
        title: 'UPV Weather',
        curveType: 'none',
        legend: { position: 'bottom' },
        hAxis: {
          title: 'Time'
        },
        vAxis: {
            maxValue: 50,
            minValue: -10,
          title: 'Temp'
        },

        backgroundColor: '#f1f8e9'
    };
    graficos.LineChart.chart = new google.visualization.LineChart(document.getElementById('line_chart'));
    graficos.LineChart.chart.draw(graficos.LineChart.data, options);
    setInterval(function() {
        makeRequest('GET', 'https://data.sparkfun.com/output/'+public_key+'.json', '', function(datos){
            data2 = JSON.parse(datos);
            var primero = data2[0]['temp'].split(".");
            graficos.Gauge.data.setValue(0, 1, primero[0]+"."+primero[1][0]);
            graficos.Gauge.chart.draw(graficos.Gauge.data, graficos.Gauge.options);

            var arr = [];
            for (el = 40; el >= 0; el--){
                var instance = data2[el];
                arr.push([new Date(instance.timestamp), parseFloat(instance.temp)]);
            }
            graficos.LineChart.data = new google.visualization.DataTable();
            graficos.LineChart.data.addColumn('date', 'X');
            graficos.LineChart.data.addColumn('number', 'Temp');
            graficos.LineChart.data.addRows(arr);
            var options = {
                title: 'UPV Weather',
                curveType: 'none',
                legend: { position: 'bottom' },
                hAxis: {
                  title: 'Time'
                },
                vAxis: {
                    maxValue: 50,
                    minValue: -10,
                  title: 'Temp'
                },
                backgroundColor: '#f1f8e9'
            };
            graficos.LineChart.chart = new google.visualization.LineChart(document.getElementById('line_chart'));
            graficos.LineChart.chart.draw(graficos.LineChart.data, options);

            var imageURI = graficos.LineChart.chart.getImageURI();
            document.getElementById('imgsrc').value = imageURI.replace("data:image/png;base64,", "");
        });
    }, 5000);
}

google.load("visualization", "1", {packages:["gauge", "corechart", "line"]});


document.onreadystatechange = function() {
    if (document.readyState == "complete") {
        google.setOnLoadCallback(drawChart);
        makeRequest('GET', 'https://data.sparkfun.com/output/'+public_key+'.json', '', function(datos){
            data2 = JSON.parse(datos);
            var primero = data2[0]['temp'].split(".");
            graficos.Gauge.data.setValue(0, 1, primero[0]+"."+primero[1][0]);
            graficos.Gauge.chart.draw(graficos.Gauge.data, graficos.Gauge.options);

            var arr = [];
            for (el = 40; el >= 0; el--){
                var instance = data2[el];
                arr.push([new Date(instance.timestamp), parseFloat(instance.temp)]);
            }
            graficos.LineChart.data = new google.visualization.DataTable();
            graficos.LineChart.data.addColumn('date', 'X');
            graficos.LineChart.data.addColumn('number', 'Temp');
            graficos.LineChart.data.addRows(arr);
            var options = {
                title: 'UPV Weather',
                curveType: 'none',
                legend: { position: 'bottom' },
                hAxis: {
                  title: 'Time'
                },
                vAxis: {
                    maxValue: 50,
                    minValue: -10,
                  title: 'Temp'
                },
                backgroundColor: '#f1f8e9'
            };
            graficos.LineChart.chart = new google.visualization.LineChart(document.getElementById('line_chart'));
            graficos.LineChart.chart.draw(graficos.LineChart.data, options);

            var imageURI = graficos.LineChart.chart.getImageURI();
            document.getElementById('imgsrc').value = imageURI.replace("data:image/png;base64,", "");
        });
    }
};



