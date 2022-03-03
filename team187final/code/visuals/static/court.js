/* Global Variables */

var loaded = false

var height = 400;
var width = 800;
var courtWidthPixels = width * 50 / 94 // assuming width = height
var basketOverhang = (48 + 15) / (94 * 12) // location of center of hoop compared to baseline
var basketLocation = { x: width / 2, y: height * basketOverhang }
var rightCourtXStart = width / 2 + courtWidthPixels / 2
window.onresize= () =>{
  if (loaded){
    var svg = d3.select("svg");
    height = $("svg").height();
    width = $("svg").width();
    console.log("resize", height, width)
    d3.select("g").attr("transform", `scale(${width/800}) translate(0,${width/50})`);
    $("svg").height(width/2);
  }
}

//This is used to apply the active class to track the state of the button group
$(document).on('click', '.btn-group-vertical input', function (e) {
  $(this).addClass('active').siblings().removeClass('active');
  //call twice to initialize and issue prediction
  success = predictSuccessThrottled();
  success = predictSuccessThrottled();
  $("#prediction").text(success);
});

window.parameters = {}
var svg = d3.select('#courtViz') //this is causing issue with no scroll bar
  .append('svg')
  .attr('width', "100%")

var courtGroup = svg.append('g')

//Need to multiple height by 2 as we're only using half of the court
var yScalePixelsToFeet = d3.scaleLinear()
  .domain([0, height*2]) //need to subtract width of lines as nitpick
  .range([0, 94])

var offenderCircle = null;
var defenderCircle = null;

/* End Global Variables */

var promises = [
  d3.json("static/backgrounds/basketball_court.json"),
  d3.json("static/backgrounds/basketball_court_markers.json"),
  languagePluginLoader,
  $.get("static/pickled_data/model_logistic_regression.pickle"),
  $.get("static/pickled_data/model_tree_classifier.pickle"),
  $.get("static/pickled_data/model_random_forest_classifier.pickle")
]

Promise.all(promises)
  .then((data) => {
    pyodide.loadPackage(['numpy']).then(() => {
      loaded = true;
      console.log("Loading complete", data)
      if (data) {
        window.courtGeo = data[0]
        window.markersGeo = data[1]
        window.parameters.model_object = data[3]
        window.parameters.model_object_tree = data[4]
        window.parameters.model_object_random_forest = data[5]
      }
      //Make an initial call of python code to initialize the model
      pyodide.runPython(pythonCode);

      //Note that you MUST call this before trying to access height/width with jquery
      // As hidden elements with always return height/width of 100
      $("#loadingWidget").fadeOut('slow')
      $("#vizPanel").fadeIn('slow')
      visualizeData();
      //Now that the svg has painted in and the data is loaded, trigger re-drawign
      window.onresize()

      //Initialize tooltips
      $(function () {
        $('[data-toggle="tooltip"]').tooltip()
      })

      //Now create the listener for form changes
      $("#parameterEntry").on("input", ()=>{
        success = predictSuccessThrottled();
        $("#prediction").text(success);
      })
    });
  });

function visualizeData() {
  console.log("Fitting to size ", height, width)
  var geoProjection = d3.geoIdentity()
    .fitSize([height, width], window.courtGeo)
    .translate([400, 25])//Note sure why this is needed, but it is
  var path = d3.geoPath().projection(geoProjection)

  courtGroup.selectAll('.court')
    .data(window.courtGeo.features)
    .enter()
    .append('path')
    .attr('d', path)
    .attr('class', 'courtLines')

  courtGroup.selectAll('.court')
    .data(window.markersGeo.features)
    .enter()
    .append('path')
    .attr('d', path)
    .attr('class', 'courtLines')

  courtGroup.append('path')
    .attr('class', 'playersPath')

  courtGroup.append('path')
    .attr('class', 'offenderBasketPath')

  createPlayers();

  success = predictSuccessThrottled();
  $("#prediction").text(success);
}

function createPlayers() {
  let playerRadius = 5;
  players = courtGroup.selectAll("circle")
    .data([
      { start_x: rightCourtXStart - courtWidthPixels/2, start_y: 75, name: "offender"},
      { start_x: rightCourtXStart - courtWidthPixels/2, start_y: 100, name: "defender"}
    ])
    .enter().append("circle")
    .attr("cx", function (d) { return d.start_x; })
    .attr("cy", function (d) { return d.start_y; })
    .attr("r", playerRadius)
    .attr("class", d => d.name)
    .on("mouseover", function (d) { d3.select(this).style("cursor", "move"); })
    .on("mouseout", function (d) { })
    .call(d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended)
    );

  //var basketCircle = svg.append('circle').attr('cx', basketLocation.x).attr('cy', basketLocation.y).attr('r', 3).attr('fill', 'black') //for testing

  offenderCircle = players._groups[0][0]
  defenderCircle = players._groups[0][1]

  drawPlayersPath();

  drawOffenderBasketPath();

  /* Begin of Drag Events */

  function dragstarted(d) {
    //d3.select(this).raise().classed("active", true); revist this
  }

  function dragged(d) {
    circle = d3.select(this)
    circle.attr("cx", d.x = d3.event.x).attr("cy", d.y = d3.event.y);

    //Update court position
    updateCourtPosition();

    drawPlayersPath();

    if (d.name == 'offender') {
      drawOffenderBasketPath();
    }
    success = predictSuccessThrottled();
    $("#prediction").text(success);
  }

  function dragended(d) {
    d3.select(this).classed("active", false);
  }

  /* End of Drag Events */

  function drawPlayersPath() {
    console.log("Drawing players path")
    let playersLineGenerator = d3.line();
    let playersLocationData = [[offenderCircle.getAttribute('cx'), offenderCircle.getAttribute('cy')], [defenderCircle.getAttribute('cx'), defenderCircle.getAttribute('cy')]]
    let playersPathString = playersLineGenerator(playersLocationData)
    console.log("Get players distance")
    let playersDistanceFeet = getDistanceBetweenPoints(playersLocationData)
    window.parameters.CLOSE_DEF_DIST = playersDistanceFeet
    $("#CLOSE_DEF_DIST").val(getFeetAndInchesString(playersDistanceFeet))

    courtGroup.selectAll('.playersPath')
      .attr('d', playersPathString)
  }

  function drawOffenderBasketPath() {
    //use this to curve offender to basket line around defender ?
    // let midPointX = (+offenderCircle.getAttribute('cx') + basketLocation.x) / 2 //hmmm
    // let midPointY = (+offenderCircle.getAttribute('cy') + basketLocation.y) / 2
    // let xAdjustmentMag = 10
    // let xAdjustment = midPointX > width / 2 ? -xAdjustmentMag : xAdjustmentMag

    let offenderBasketLineGenerator = d3.line();
    let offenderBasketLocations = [[offenderCircle.getAttribute('cx'), offenderCircle.getAttribute('cy')],
    //[midPointX + xAdjustment, midPointY],
    [basketLocation.x, basketLocation.y]]
    let offenderBasketLineString = offenderBasketLineGenerator(offenderBasketLocations)
    offenderBasketDistance = getDistanceBetweenPoints(offenderBasketLocations)
    window.parameters.SHOT_DIST = offenderBasketDistance
    $("#SHOT_DIST").val(getFeetAndInchesString(offenderBasketDistance))

    courtGroup.selectAll('.offenderBasketPath')
      .attr('d', offenderBasketLineString)
  }

  function getDistanceBetweenPoints([[x1, y1], [x2, y2]]) {
    let distance = Math.sqrt(Math.pow(+x2 - +x1, 2) + Math.pow(+y2 - +y1, 2))
    let distanceInFeet = yScalePixelsToFeet(distance)
    return distanceInFeet
  }

  function getFeetAndInchesString(feetAsDecimal) {
    let feet = Math.floor(feetAsDecimal)
    let inches = Math.round((feetAsDecimal - feet) * 12)
    return feet + "FT" + " " + inches + "IN"
  }
}

function predictSuccess() {
  window.parameters.SHOT_NUMBER = parseInt($("#SHOT_NUMBER").val());
  window.parameters.PERIOD = parseInt($("#PERIOD").val());
  window.parameters.TOUCH_TIME = parseInt($("#TOUCH_TIME").val());
  window.parameters.DRIBBLES = parseInt($("#DRIBBLES").val());
  window.parameters.POS_TIME_REMAINING = parseInt($("#POS_TIME_REMAINING").val());
  window.parameters.SHOT_TYPE = $("#SHOT_TYPE").val();
  window.parameters.SHOT_ZONE = $("#SHOT_ZONE").val();
  //Pass state of player information UI to python/model
  console.log(window.parameters);
  switch ($("#model_button_group .active").attr("id")) {
    case "logistic_regression":
      return pyodide.runPython(pythonCode);
    case "decision_tree":
      return pyodide.runPython(pythonCode_decisionTree);
    case "random_forest":
      return pyodide.runPython(pythonCode_randomForest);
  }

};
predictSuccessThrottled = _.throttle(predictSuccess, 100);

function matrix(a, b, c, d, tx, ty) {
  return d3.geoTransform({
    point: function (x, y) {
      this.stream.point(a * x + b * y + tx, c * x + d * y + ty);
    }
  });
}

function updateCourtPosition() {
  let x = yScalePixelsToFeet(offenderCircle.getAttribute('cx'))
  let y = yScalePixelsToFeet(offenderCircle.getAttribute('cy'))
  console.log("Location: ", x, y)
  //center of court is x = 47, y = 42
  // mid court lines at y = 24.4
  //3 point line is at (47, 25), (26.3, 11.1), (67.6, 11)
  let courtLocation = getCourtLocation(x, y)
  console.log(courtLocation)
  $("#SHOT_ZONE").val(courtLocation)
}

function getCourtLocation(x, y) {
  x = x-47
  y = y-3
  if (y > 39.9) {
    return "Back Court(BC)"
  }
  //Right
  if (x > 12.5) {
    if (y < 8.8) {
      return "Right Side(R)"
    } else {
      return "Right Side Center(RC)"
    }
  }
  //Left
  else if (x < -12.5) {
    if (y < 8.8) {
      return "Left Side(L)"
    } else {
      return "Left Side Center(LC)"
    }
  }
  else {
    return "Center(C)"
  }
  return "None"
}
// shot_zone_area,    min_x,  max_x,  min_y ,max_y
// Back Court(BC),    -22.5,  23.4,   39.9, 85.2 XXXXXX
// Center(C),         -12.5,  12.2,   -5.1, 39.7 XXXXXX
// Left Side Center(LC),5.1,  24.3,   8.8,  39.7
// Left Side(L),       4.1,   25,     -4.3, 13.8
// Right Side Center(RC)-24.7,-5,     8.8,  39.5
// Right Side(R),       -25,  -4.2,   -4.1, 13.8

//references
//https://team.carto.com/u/aromeu/datasets
//https://proformancehoops.com/basketball-court-dimensions/
