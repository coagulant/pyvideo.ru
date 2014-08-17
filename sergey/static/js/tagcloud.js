var fill = d3.scale.category20();


function draw(words) {
    d3.select("#hell").append("svg")
        .attr("width", width)
        .attr("height", height)
      .append("g")
        .attr("transform", "translate(" + width/2 + ", " + height/2 + ")")
      .selectAll("text")
        .data(words)
      .enter()
        .append("svg:a")
            .attr("xlink:href", function(d) { return d.link; })
        .append("text")
        .style("font-size", function(d) { return d.size + "px"; })
        .style("font-family", "Impact")
        .style("fill", function(d, i) { return fill(i); })
        .attr("text-anchor", "middle")
        .attr("transform", function(d) {
          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function(d) { return d.text; })
      .on("click", function(d) {
            console.log(d.text);
        });
}


function getSize(numVideos, totalVideos) {
    if (numVideos > 10) {
        return 30;
    } else if (numVideos > 5) {
        return 20;
    } else if (numVideos > 2) {
        return 15;
    } else {
        return 10;
    }
}
