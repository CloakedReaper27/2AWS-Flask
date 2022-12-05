// start chart js
const ctx = document.getElementById("myChart");
        
      new Chart(ctx, {
        type: "line",
        data: {
          labels: ["miss rate", "hit rate", "no. of items", "total size", "no of requests per min"],
          datasets: [
            {
              label: "# of Votes",
              data: [12, 19, 3, 5, 2, 3],
              backgroundColor: [
                "rgb(255, 99, 132)",
                "rgb(54, 162, 235)",
                "rgb(255, 205, 86)",
              ],
              borderWidth: 5,
              yAxisID: 'y',
            },
            {
              label: "# of Votes",
              data: [2, 9, 3, 5, 5,13],
              backgroundColor: [
                "rgb(255, 99, 132)",
                "rgb(54, 162, 235)",
                "rgb(255, 205, 86)",
              ],
              borderWidth: 5,
              borderColor:'rgb(54, 162, 235)',
              yAxisID: 'y1',
            },
            {
              label: "# of Votes",
              data: [ 5, 5,13,2, 9, 3,],
              backgroundColor: [
                "rgb(255, 99, 132)",
                "rgb(54, 162, 235)",
                "rgb(255, 205, 86)",
              ],
              borderWidth: 5,
              borderColor:'rgb(255, 205, 86)',
              yAxisID: 'y2',
            },
            {
              label: "# of Votes",
              data: [2, 13,9, 3, 5, 5],
              backgroundColor: [
                "rgb(255, 99, 132)",
                "rgb(54, 162, 235)",
                "rgb(255, 205, 86)",
              ],
              borderWidth: 5,
              borderColor:'rgb(255, 99, 132)',
              yAxisID: 'y3',
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