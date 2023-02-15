var date = {'Date': ['02-01-2023', '02-02-2023', '02-03-2023', '02-04-2023', '02-05-2023', '02-06-2023', '02-07-2023', '02-08-2023', '02-09-2023', '02-10-2023', '02-11-2023', '02-12-2023', '02-13-2023', '02-14-2023', '02-15-2023']}
var solar_energy_exported = {'kWhCreated': [17.27, 28.31, 20.88, 31.01, 26.15, 23.7, 16.58, 23.77, 26.0, 8.82, 27.06, 31.2, 20.53, 27.74, 28.72]}
var total_consumer_energy = {'kWhUsed': [15.47, 21.74, 21.16, 17.62, 20.89, 14.42, 16.39, 17.0, 13.18, 13.78, 18.37, 15.48, 13.22, 19.51, 13.82]}
var lifetime_solar_energy_exported = 361.51
var lifetime_solar_energy_exported_value = 112
var consumer_energy_imported_from_grid = {'kWh': [10.96, 8.69, 13.66, 10.37, 14.63, 8.56, 8.93, 11.33, 7.12, 8.96, 10.99, 8.23, 8.26, 7.66, 7.62]}
var consumer_energy_imported_from_solar = {'kWh': [4.51, 13.05, 7.5, 7.25, 6.26, 5.86, 7.46, 5.67, 6.06, 4.82, 7.38, 7.25, 4.96, 11.85, 6.2]}
var lifetime_net_energy_exported_grid = 150
var lifetime_net_energy_exported_grid_value = 39




Apex.grid = {
  padding: {
    right: 0,
    left: 0
  }
}

Apex.dataLabels = {
  enabled: false
}

var randomizeArray = function (arg) {
  var array = arg.slice();
  var currentIndex = array.length, temporaryValue, randomIndex;

  while (0 !== currentIndex) {

    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}

// data for the sparklines that appear below header area
var sparklineData = [47, 45, 54, 38, 56, 24, 65, 31, 37, 39, 62, 51, 35, 41, 35, 27, 93, 53, 61, 27, 54, 43, 19, 46];

// the default colorPalette for this dashboard
//var colorPalette = ['#01BFD6', '#5564BE', '#F7A600', '#EDCD24', '#F74F58'];
var colorPalette = ['#00D8B6','#008FFB',  '#FEB019', '#FF4560', '#775DD0']

var spark1 = {
  chart: {
    id: 'sparkline1',
    group: 'sparklines',
    type: 'area',
    height: 160,
    sparkline: {
      enabled: true
    },
  },
  stroke: {
    curve: 'straight'
  },
  fill: {
    opacity: 1,
  },
  series: [{
    name: 'kWh',
    // data: randomizeArray(sparklineData)
    data: solar_energy_exported.kWhCreated
  }],
  labels: date.Date,
  yaxis: {
    min: 0
  },
  xaxis: {
    type: 'datetime',
    categories: date.Date,
  },
  colors: ['#DCE6EC'],
  title: {
    text: lifetime_solar_energy_exported,
    offsetX: 30,
    style: {
      fontSize: '24px',
      cssClass: 'apexcharts-yaxis-title'
    }
  },
  subtitle: {
    text: 'Total Produced (kWh)',
    offsetX: 30,
    style: {
      fontSize: '14px',
      cssClass: 'apexcharts-yaxis-title'
    }
  }
}

var spark2 = {
  chart: {
    id: 'sparkline2',
    group: 'sparklines',
    type: 'area',
    height: 160,
    sparkline: {
      enabled: true
    },
  },
  stroke: {
    curve: 'straight'
  },
  fill: {
    opacity: 1,
  },
  series: [{
    name: 'Net Energy Exported (kWH)',
    data: randomizeArray(sparklineData)
  }],
  labels: [...Array(24).keys()].map(n => `2018-09-0${n+1}`),
  yaxis: {
    min: 0
  },
  xaxis: {
    type: 'datetime',
  },
  colors: ['#DCE6EC'],
  title: {
    text: lifetime_net_energy_exported_grid + "   ($" + lifetime_net_energy_exported_grid_value + ")",
    offsetX: 30,
    style: {
      fontSize: '24px',
      cssClass: 'apexcharts-yaxis-title'
    }
  },
  subtitle: {
    text: 'Net Energy Exported (kWH)',
    offsetX: 30,
    style: {
      fontSize: '14px',
      cssClass: 'apexcharts-yaxis-title'
    }
  }
}

// var spark3 = {
//   chart: {
//     id: 'sparkline3',
//     group: 'sparklines',
//     type: 'donut',
//     // height: 160,
//     // sparkline: {
//     //   enabled: true
//     // },
//   },
//   series: [1],
//   labels: ["Days Stashed"],
//   plotOptions: {
//     pie: {
//       donut: {
//         labels: {
//           show: true,
//         }
//       },
//       size: 200
//     }
//   },
//   dataLabels: {
//     enabled: false,
//   }
// }

var spark3 = {
  chart: {
    id: 'sparkline3',
    group: 'sparklines',
    type: 'donut',
    height: 160,
    sparkline: {
      enabled: true
    },
  },
  stroke: {
    curve: 'straight'
  },
  fill: {
    opacity: 1,
  },
  series: [{
    name: 'Days Stashed',
    data: randomizeArray(sparklineData)
  }],
  labels: [...Array(24).keys()].map(n => `2018-09-0${n+1}`),
  xaxis: {
    type: 'datetime',
  },
  yaxis: {
    min: 0
  },
  colors: ['#008FFB'],
  title: {
    text: Math.round(lifetime_net_energy_exported_grid/17),
    offsetX: 30,
    style: {
      fontSize: '24px',
      cssClass: 'apexcharts-yaxis-title'
    }
  },
  subtitle: {
    text: 'Days Stashed',
    offsetX: 30,
    style: {
      fontSize: '14px',
      cssClass: 'apexcharts-yaxis-title'
    }
  }
}


new ApexCharts(document.querySelector("#spark1"), spark1).render();
new ApexCharts(document.querySelector("#spark2"), spark2).render();
new ApexCharts(document.querySelector("#spark3"), spark3).render();


var optionsArea = {
  title: {
    text: "kWH Produced vs. Used"
  },
  series: [{
  name: 'kWh Produced',
  data: solar_energy_exported.kWhCreated
}, {
  name: 'kWh Used',
  data: total_consumer_energy.kWhUsed
}],
  chart: {
  height: 350,
  type: 'area'
},
dataLabels: {
  enabled: false
},
stroke: {
  curve: 'smooth'
},
xaxis: {
  type: 'datetime',
  categories: date.Date
},
yaxis: {
  labels: {
    formatter: (value) => {
      return value.toFixed(0)
    },
  }
},
legend: {
  itemMargin: {
    horizontal: 10,
    vertical: 10
  },
},
tooltip: {
  x: {
    format: 'MM/dd/yy'
  },
},
};

var chartArea = new ApexCharts(document.querySelector("#area"), optionsArea);
chartArea.render();

var optionsBar = {
  chart: {
    type: 'bar',
    height: 380,
    width: '100%',
    stacked: true,
  },
  plotOptions: {
    bar: {
      columnWidth: '45%',
    }
  },
  colors: colorPalette,
  series: [{
    name: "Clothing",
    data: [42, 52, 16, 55, 59, 51, 45, 32, 26, 33, 44, 51, 42, 56],
  }, {
    name: "Food Products",
    data: [6, 12, 4, 7, 5, 3, 6, 4, 3, 3, 5, 6, 7, 4],
  }],
  labels: [10,11,12,13,14,15,16,17,18,19,20,21,22,23],
  xaxis: {
    labels: {
      show: false
    },
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false
    },
  },
  yaxis: {
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false
    },
    labels: {
      style: {
        colors: '#78909c'
      }
    }
  },
  title: {
    text: 'Monthly Sales',
    align: 'left',
    style: {
      fontSize: '18px'
    }
  }

}

var chartBar = new ApexCharts(document.querySelector('#bar'), optionsBar);
chartBar.render();


var optionDonut = {
  chart: {
      type: 'donut',
      width: '100%',
      height: 400
  },
  dataLabels: {
    enabled: false,
  },
  plotOptions: {
    pie: {
      customScale: 0.8,
      donut: {
        size: '75%',
      },
      offsetY: 20,
    },
    stroke: {
      colors: undefined
    }
  },
  colors: colorPalette,
  title: {
    text: 'Department Sales',
    style: {
      fontSize: '18px'
    }
  },
  series: [21, 23, 19, 14, 6],
  labels: ['Clothing', 'Food Products', 'Electronics', 'Kitchen Utility', 'Gardening'],
  legend: {
    position: 'left',
    offsetY: 80
  }
}

var donut = new ApexCharts(
  document.querySelector("#donut"),
  optionDonut
)
donut.render();


function trigoSeries(cnt, strength) {
  var data = [];
  for (var i = 0; i < cnt; i++) {
      data.push((Math.sin(i / strength) * (i / strength) + i / strength+1) * (strength*2));
  }

  return data;
}



// var optionsLine = {
//   chart: {
//     height: 340,
//     type: 'line',
//     zoom: {
//       enabled: false
//     }
//   },
//   plotOptions: {
//     stroke: {
//       width: 4,
//       curve: 'smooth'
//     },
//   },
//   colors: colorPalette,
//   series: [
//     {
//       name: "Day Time",
//       data: trigoSeries(52, 20)
//     },
//     {
//       name: "Night Time",
//       data: trigoSeries(52, 27)
//     },
//   ],
//   title: {
//     floating: false,
//     text: 'Customers',
//     align: 'left',
//     style: {
//       fontSize: '18px'
//     }
//   },
//   subtitle: {
//     text: '168,215',
//     align: 'center',
//     margin: 30,
//     offsetY: 40,
//     style: {
//       color: '#222',
//       fontSize: '24px',
//     }
//   },
//   markers: {
//     size: 0
//   },

//   grid: {

//   },
//   xaxis: {
//     labels: {
//       show: false
//     },
//     axisTicks: {
//       show: false
//     },
//     tooltip: {
//       enabled: false
//     }
//   },
//   yaxis: {
//     tickAmount: 2,
//     labels: {
//       show: false
//     },
//     axisBorder: {
//       show: false,
//     },
//     axisTicks: {
//       show: false
//     },
//     min: 0,
//   },
//   legend: {
//     position: 'top',
//     horizontalAlign: 'left',
//     offsetY: -20,
//     offsetX: -30
//   }

// }

// var chartLine = new ApexCharts(document.querySelector('#line'), optionsLine);

// a small hack to extend height in website sample dashboard
chartLine.render().then(function () {
  var ifr = document.querySelector("#wrapper");
  if (ifr.contentDocument) {
    ifr.style.height = ifr.contentDocument.body.scrollHeight + 20 + 'px';
  }
});


// on smaller screen, change the legends position for donut
var mobileDonut = function() {
  if($(window).width() < 768) {
    donut.updateOptions({
      plotOptions: {
        pie: {
          offsetY: -15,
        }
      },
      legend: {
        position: 'bottom'
      }
    }, false, false)
  }
  else {
    donut.updateOptions({
      plotOptions: {
        pie: {
          offsetY: 20,
        }
      },
      legend: {
        position: 'left'
      }
    }, false, false)
  }
}

$(window).resize(function() {
  mobileDonut()
});
