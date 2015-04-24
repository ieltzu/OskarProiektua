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

makeRequest('GET', 'https://data.sparkfun.com/output/'+public_key+'.json', '', function(data){
        var data2 = JSON.parse(data);
        temperatura = data2[0]['temp'];
}, false);

function drawChart() {

            var data = google.visualization.arrayToDataTable([
                ['Label', 'Value'],
                ['Temp', temperatura],
                ]);

            var options = {
              width: 400, height: 120,
              redFrom: 90, redTo: 100,
              yellowFrom:75, yellowTo: 90,
              minorTicks: 5
            };

            var chart = new google.visualization.Gauge(document.getElementById('chart_div'));

            chart.draw(data, options);

            var arr = [];
            for (el in data2){
                var instance = data2.pop();
                arr.push([parseFloat(el), parseFloat(instance.temp)]);
            }
            var data = new google.visualization.DataTable();
            data.addColumn('number', 'X');
            data.addColumn('number', 'Temp');
            data.addRows(arr);
            var options = {
                title: 'UPV Weather',
                curveType: 'none',
                legend: { position: 'bottom' },
                hAxis: {
                  title: 'Time'
                },
                vAxis: {
                  title: 'Temp'
                },
                backgroundColor: '#f1f8e9'
            };
            var chart = new google.visualization.LineChart(document.getElementById('line_chart'));
            chart.draw(data, options);

            setInterval(function() {
                makeRequest('GET', 'https://data.sparkfun.com/output/'+public_key+'.json', '', function(datos){
                    var datos = JSON.parse(datos);
                    data.setValue(0, 1, datos[0]['temp']);
                    chart.draw(data, options);
                });
                data.setValue(0, 1, temperatura);
                chart.draw(data, options);
                drawLineChart();
            }, 5000);
        }

        google.load("visualization", "1", {packages:["gauge", "corechart", "line"]});

        google.setOnLoadCallback(drawChart);

var data2 =[];
document.onreadystatechange = function() {
    if (document.readyState == "complete") {

        /*setInterval(function(){
            makeRequest('GET', 'https://data.sparkfun.com/output/'+public_key+'.json', '', function(data){
                data2 = JSON.parse(data);
                console.log(data2);
                temperatura = data2[0]['temp'];
            });
        }, 5000);

        /*document.getElementById('dropb').addEventListener("click", function(event){
        });
        document.getElementById('twitb').addEventListener("click", function(event){
        });*/

    }
};


