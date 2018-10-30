function parseData(data) {
    var datetimeFormat = d3.isoFormat;

    var arr = [];
    for (var i in data) {
        arr.push(
            {
                date: d3.isoParse(data[i][0]),
                value: data[i][1]
            }
        );
    }
    return arr;
}

var data = parseData([["2018-10-29T20:32:06.418", "15.56"], ["2018-10-29T20:40:16.913", "17.20"], ["2018-10-29T21:06:10.458", "19.32"], ["2018-10-30T19:01:40.271", "20.19"], ["2018-10-30T19:02:12.081", "16.60"]])

var svgWidth = 640, svgHeight = 480;
var margin = { top: 20, right: 20, bottom: 50, left: 50 };
var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;
var svg = d3.select('svg')
 .attr("width", svgWidth)
 .attr("height", svgHeight);

var g = svg.append("g")
.attr("transform",
  "translate(" + margin.left + "," + margin.top + ")"
);

var x = d3.scaleTime().rangeRound([0, width]);
var y = d3.scaleLinear().rangeRound([height, 0]);


var line = d3.line()
    .x(function(d) { return x(d.date)})
    .y(function(d) { return y(d.value)});

x.domain(d3.extent(data, function(d) { console.log(d.date); return d.date }));
y.domain(d3.extent(data, function(d) { return d.value }));

g.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x))
    .select(".domain")
    .remove();

g.append("g")
   .call(d3.axisLeft(y))
   .append("text")
   .attr("fill", "#000")
   .attr("transform", "rotate(-90)")
   .attr("y", 6)
   .attr("dy", "0.71em")
   .attr("text-anchor", "end")
   .text("Temperatura (°C)");

g.append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-linejoin", "round")
    .attr("stroke-linecap", "round")
    .attr("stroke-width", 1.5)
    .attr("d", line);