// start chart js

var geo0 = JSON.parse(document.getElementById("mydiv").dataset.geo0);
var geo1 = JSON.parse(document.getElementById("mydiv1").dataset.geo1);
var geo2 = JSON.parse(document.getElementById("mydiv2").dataset.geo2);
var geo3 = JSON.parse(document.getElementById("mydiv3").dataset.geo3);
var geo4 = JSON.parse(document.getElementById("mydiv4").dataset.geo4);
// var workers = JSON.parse(document.getElementById("workers").dataset.work);


const ctx = document.getElementById("myChart");
      new Chart(ctx, {
        type: "line",
        data: {
          labels: ["30:00", "1:00:00", "1:30:00", "2:00:00", "2:30:00"],
          datasets: [
            {
              label: "no of workers",
              data: [geo0[5],geo1[5],geo2[5],geo3[5],geo4[5]],
              backgroundColor: [
                "rgb(255, 99, 132)",
                "rgb(54, 162, 235)",
                "rgb(255, 205, 86)",
              ],
              borderWidth: 5,
              borderColor:'rgb(255, 99, 12)',
              yAxisID: 'y',
            },
            {
              label: "miss rate",
              data: [geo0[3],geo1[3],geo2[3],geo3[3],geo4[3]],
              backgroundColor: [
                "rgb(255, 99, 132)",
                "rgb(54, 162, 235)",
                "rgb(255, 205, 86)",
              ],
              borderWidth: 5,
              yAxisID: 'y',
            },
            {
              label: "hit rate",
              data: [geo0[4],geo1[4],geo2[4],geo3[4],geo4[4]],
              backgroundColor: [
                "rgb(255, 99, 132)",
                "rgb(54, 162, 235)",
                "rgb(255, 205, 86)",
              ],
              borderWidth: 5,
              borderColor:'rgb(54, 162, 235)',
              yAxisID: 'y',
            },
            {
              label: "no. of items",
              data: [geo0[0],geo1[0],geo2[0],geo3[0],geo4[0]],
              backgroundColor: [
                "rgb(255, 99, 132)",
                "rgb(54, 162, 235)",
                "rgb(255, 205, 86)",
              ],
              borderWidth: 5,
              borderColor:'rgb(255, 205, 86)',
              yAxisID: 'y',
            },
            {
              label: "total size",
              data: [geo0[2],geo1[2],geo2[2],geo3[2],geo4[2]],
              backgroundColor: [
                "rgb(255, 99, 132)",
                "rgb(54, 162, 235)",
                "rgb(255, 205, 86)",
              ],
              borderWidth: 5,
              borderColor:'rgb(255, 9, 132)',
              yAxisID: 'y',
            },
			      {
              label: "no of requests per min",
              data: [geo0[1],geo1[1],geo2[1],geo3[1],geo4[1]],
              backgroundColor: [
                "rgb(255, 99, 132)",
                "rgb(54, 162, 235)",
                "rgb(255, 205, 86)",
              ],
              borderWidth: 5,
              borderColor:'rgb(25, 9, 132)',
              yAxisID: 'y',
            },
			      
          ],
        },
        options: {
    responsive: true,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    stacked: false,
    plugins: {
      title: {
        display: true,
        text: 'Chart.js Line Chart - Multi Axis'
      },
    },
    scales: {
      y: {
        type: 'linear',
        display: true,
        position: 'left',
      },
      y1: {
        type: 'linear',
        display: false,
        position: 'right',

        // grid line settings
        grid: {
          drawOnChartArea: false, // only want the grid lines for one axis to show up
          
        },
      },
      y2: {
        type: 'linear',
        display: false,
        position: 'right',

        // grid line settings
        grid: {
          drawOnChartArea: false, // only want the grid lines for one axis to show up
        },
      },
      y3: {
        type: 'linear',
        display: false,
        position: 'right',

        // grid line settings
        grid: {
          drawOnChartArea: false, // only want the grid lines for one axis to show up
        },
      },
    }
  },
      });

    //   end chart js
     
    // start code js
    var current = 0;
    const min = 62.5;
    const max = 500;
    var size = 0;
    var btnIncrease = document.getElementById("btnIncrease");
    var btnDecrease = document.getElementById("btnDecrease");
    var progressBar =
      document.getElementsByClassName("progress-container");

    // start range
    var slider = document.querySelector(".memoryCapacity #range");
    var output = document.querySelector(".memoryCapacity #demo");
    output.innerHTML = slider.value;
    slider.oninput = function () {
      output.innerHTML = this.value;
    };
    var maxmiss = document.querySelector(".maxmiss #range");
    var maxmissOut = document.querySelector(".maxmiss #demo");
    maxmissOut.innerHTML = maxmiss.value;
    maxmiss.oninput = function () {
      maxmissOut.innerHTML = this.value;
    };
    var minmiss = document.querySelector(".minmiss #range");
    var minmissOut = document.querySelector(".minmiss #demo");
    minmissOut.innerHTML = minmiss.value;
    minmiss.oninput = function () {
      minmissOut.innerHTML = this.value;
    };
    // end range

    // start ProgressPar
    btnIncrease.addEventListener("click", (e) => {
    
      if (current < max) {
        current = current + 62.5;
        size++;
      }
    });
    btnDecrease.addEventListener("click", (e) => {
     
      if (current > min) {
        size--;
        current = current - 62.5;
      }
    });
    // end ProgressPar

    // start select mode
    let divs = document.querySelector(".progression");
    let divs2 = document.querySelector(".threshold");
    let choices = document.querySelectorAll(".mode .radio input");

    choices[0].addEventListener("click", function (e) {
      divs.style.display = "block";
      divs2.style.display = "none";
    });

    choices[1].addEventListener("click", function (e) {
      divs2.style.display = "flex";
      divs.style.display = "none";
    });
    // end select mode