var w = 6000,
    h = 4000;

var tree = d3.layout.tree()
    .size([h - 1000, w]);

var diagonal = d3.svg.diagonal()
    .projection(function(d) { return [d.y, d.x]; });

function Popup (text, d, i) {
	this.div = d3.select("body").append("div").attr("class", "popup").attr("data-node", i);
	this.node = d;
	this.index = i;
	this.inner = this.div.append("span").attr("class", "popupText");
	this.showing = false;
	this.display = function(d) {
		this.inner.text(text);
		this.div.style("display", "block");
		this.update(d);
		this.showing = true;
		return this;
	};
	this.update = function (d) {
		this.div.style("left", Math.floor(d.y + 210) + "px");
		this.div.style("top", Math.floor(d.x + 110)  + "px");
	};
	this.hide = function(d) {
		this.update(d);
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

var displayText = function (d, i) {
	if (!("popup" in d)) {
	// check for orphaned popup first
		try {
			var pop = d3.selectAll(".popup");
			if (!pop.empty()) {
				pop.each(function () {
					if (this.dataset["node"] == i) this.parentNode.removeChild(this);
				});
			}
		}	
		catch (e) {}
	
		myText = d.text + "\n" + d.signature;
		d.popup = new Popup(myText, d, i).display(d);
	}
	else {
		if (d.popup.showing) {
			d.popup.hide(d);
		}
		else {
			d.popup.display(d);
		}
	}
}


var duration = 2000;
var nodes, treeScale, treeAxis, timeAxis;


// setup

d3.json("okp.json", function(json) {

  nodes = tree.nodes(json);
  treeScale = d3.scale.linear()
  	.range([0, w])
  	.domain([0,11]);
  	

   treeAxis = d3.svg.axis()
	.scale(treeScale)
	.tickSize(h)
	.orient("top");
	timeAxis =	d3.svg.axis()
			.scale(timeScale)
			.tickSize(h)
			.tickFormat(d3.time.format("%b %e"))
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
      .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });
          	
				
  node.append("circle")
      .attr("r", 4.5)
      .style("fill", function(d) { if (d.author == 1) {return "#0e0";} else {return "#fff"; }})
	.on("click", displayText);
	
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


function nodeTransition(selection) {
	selection.transition()
			.duration(duration)
			.attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });
}
function linkTransition(selection) {
	selection.transition()
			.duration(duration)
			.attr("d", diagonal);
}

function popupsUpdate() {
		try {
			var pop = d3.selectAll(".popup");
			if (!pop.empty()) {
				pop.transition()
				.duration(duration)
				.style("left", function (d, i) { return Math.floor(nodes[this.dataset["node"]].y + 210) + "px" })
				.style("top", function (d, i) { return Math.floor(nodes[this.dataset["node"]].x + 110) + "px" });
			}
		}
		catch (e) { console.log(e) }
}

function update(timeline) {
	
	d3.select(".depth")
		.attr("class", timeline ? "depth first" : "depth first active");
	d3.select(".time")
		.attr("class", timeline ? "time last active" : "time last");

	var node = vis.selectAll("g.node");
	var link = vis.selectAll("path.link");
		
	if (timeline) {
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
		link.call(linkTransition);
		node.call(nodeTransition);
		popupsUpdate();
	}
	
	else {
		d3.json("okp.json", function(json) {
			nodes = tree.nodes(json);
			link.data(tree.links(nodes)).call(linkTransition);
			node.data(nodes).call(nodeTransition);
			d3.selectAll("circle").data(nodes);
			popupsUpdate();
		});
	}



		d3.select(".x.axis")
			.transition()
			.duration(duration)
			.call(timeline ? timeAxis : treeAxis);
			
		d3.select(".axislabel")
			.text(timeline ? "Date:" : "Reply depth:");
			
		vis.selectAll(".tick")
			.attr("display", timeline ? "block" : "none");

	
	
}