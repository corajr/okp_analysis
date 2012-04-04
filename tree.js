var w = 6000,
    h = 4000;

var tree = d3.layout.tree()
    .size([h - 1000, w]);

var diagonal = d3.svg.diagonal()
    .projection(function(d) { return [d.y, d.x]; });

function Popup (text) {
	this.div = d3.select("body").append("div").attr("class", "popup");
	this.inner = this.div.append("span").attr("class", "popupText");
	this.showing = false;
	this.display = function(d) {
		this.inner.text(text);
		this.div.style("display", "block");
		this.div.style("left", Math.floor(d.y + 210) + "px");
		this.div.style("top", Math.floor(d.x + 110)  + "px");
		this.showing = true;
	};
	this.hide = function() {
		this.div.style("display", "none");
		this.showing = false;
	};
};


var vis = d3.select("#chart").append("svg")
    .attr("width", w)
    .attr("height", h)
    .append("g")
    .attr("transform", "translate(200, 100)");

var earliestDate = new Date("2007-11-18T08:42:00+00:00");
// var latestDate = new Date("2007-12-13T05:53:00+00:00");
var latestDate = new Date("2007-11-27T05:53:00+00:00");
var timeScale = d3.time.scale()
				.domain([earliestDate, latestDate])
				.range([0,w]);

var displayText = function (d) {
	if (!("popup" in d)) {
		myText = d.text + "\n" + d.signature;
		d.popup = new Popup(myText);
	}
	if (d.popup.showing) {
		d.popup.hide();
	}
	else {
		d.popup.display(d);
	}
}


var duration = 2000;
var nodes, treeScale, treeAxis, timeAxis;


d3.json("okp.json", function(json) {
  nodes = tree.nodes(json);
  treeScale = d3.scale.linear()
  	.range([0, w])
  	.domain([0,11]);
  	

   treeAxis = d3.svg.axis()
	.scale(treeScale)
	.tickSize(h)
	.orient("top");
  
  var link = vis.selectAll("path.link")
      .data(tree.links(nodes))
    .enter().append("path")
      .attr("class", "link")
      .attr("d", diagonal);

	vis.append("svg:g")
		  .attr("class", "x axis")
		  .attr("transform", "translate(0," + (h - 50) + ")")	  
		.call(treeAxis);
		
  var node = vis.selectAll("g.node")
      .data(nodes)
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; })
          	.on("click", displayText);
				
  node.append("circle")
      .attr("r", 4.5)
      .style("fill", function(d) { if (d.author == 1) {return "#0e0";} else {return "#fff"; }})

   node.append("text")
       .attr("dx", function(d) { return d.children ? -8 : 8; })
       .attr("dy", 3)
       .attr("text-anchor", function(d) { return d.children ? "end" : "start"; })
       .text(function(d) { return d.name; });

	vis.append("text")
		.attr("class", "axislabel")
		.attr("x", -200)
		.attr("y", -50)
		.text("Reply depth:");


	vis.selectAll(".tick")
		.attr("display", "none");
});

function update(timeline) {
	if (timeline) {
		d3.select(".depth")
			.attr("class", "depth first");
		d3.select(".time")
			.attr("class", "time last active");

		
		timeAxis =	d3.svg.axis()
			.scale(timeScale)
			.tickSize(h)
			.orient("top");

	  for (i in nodes) {
		nodes[i].y = timeScale(new Date(nodes[i].date_time));
		nodes[i].x *= 1.5
 		if (i-1 in nodes) {
 			if (Math.abs(nodes[i-1].x - nodes[i].x) < 10) {
 				nodes[i-1].x -= 10
 				nodes[i].x += 10
 			}
 		}
	}

	  var link = vis.selectAll("path.link")
			.transition()
			.duration(duration)
			.attr("d", diagonal);
			
		d3.select(".x.axis")
			.transition()
			.duration(duration)
			.call(timeAxis);
			
		d3.select(".axislabel")
			.text("Date:");
		vis.selectAll(".tick")
			.attr("display", "block");

			  
		var node = vis.selectAll("g.node")
			.transition()
			.duration(duration)
			.attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });
		}
	else {	//reset
	
		d3.select(".depth")
			.attr("class", "depth first active");
		d3.select(".time")
			.attr("class", "time last");

		d3.json("okp.json", function(json) {
		
		  nodes = tree.nodes(json);
		  
	var node = vis.selectAll("g.node")
		.data(nodes)
		.transition()
		.duration(duration)
		.attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });
	
	var pop = d3.selectAll(".popup");
	if (pop.length >= 1) {
		pop.transition()
		.duration(duration)
		.style("left", function (d) { return  Math.floor(d.y + 210) + "px" })
		.style("top", function (d) { return  Math.floor(d.y + 110) + "px" });
	}	
	
	
	  var link = vis.selectAll("path.link")
	  	.data(tree.links(nodes))
		.transition()
		.duration(duration)
		.attr("d", diagonal);
		});
		
		d3.select(".x.axis")
			.transition()
			.duration(duration)
			.call(treeAxis);
			
		d3.select(".axislabel")
			.text("Reply depth:");
			
		vis.selectAll(".tick")
		.attr("display", "none");
	}
}