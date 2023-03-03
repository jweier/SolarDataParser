var lifetime_energy_imported_from_everywhere = 456.71
var lifetime_net_energy = 68
var lifetime_net_energy_value = 18
var lifetime_solar_energy_exported = 525
var lifetime_solar_energy_exported_value = 163
var lifetime_avg_daily_electricity_usage = 15.75
var lifetime_avg_daily_produced_by_solar = 18.11
var timestamp = ['02-01-2023', '02-02-2023', '02-03-2023', '02-04-2023', '02-05-2023', '02-06-2023', '02-07-2023', '02-08-2023', '02-09-2023', '02-10-2023', '02-11-2023', '02-12-2023', '02-13-2023', '02-14-2023', '02-15-2023', '02-16-2023', '02-17-2023', '02-18-2023', '02-19-2023', '02-20-2023', '02-21-2023', '02-22-2023', '02-23-2023', '02-24-2023', '02-25-2023', '02-26-2023', '03-01-2023', '03-02-2023', '03-03-2023']
var solar_energy_exported = ['17.27', '28.31', '20.88', '31.01', '26.15', '23.70', '16.58', '23.77', '26.00', '8.82', '27.06', '31.20', '20.53', '27.74', '28.72', '24.01', '11.80', '3.68', '28.84', '15.39', '20.10', '2.31', '8.38', '0.44', '20.58', '13.39', '2.22', '9.40', '6.82']
var grid_energy_imported = ['10.96', '8.69', '13.66', '10.37', '14.63', '8.56', '8.93', '11.33', '7.12', '8.96', '10.99', '8.23', '8.26', '7.66', '7.62', '8.69', '6.19', '8.36', '7.40', '8.77', '9.22', '11.38', '12.45', '15.27', '10.23', '7.95', '13.85', '7.34', '9.47']
var grid_energy_exported_from_solar = ['12.76', '15.26', '13.38', '23.76', '19.89', '17.84', '9.12', '18.10', '19.94', '4.00', '19.68', '23.95', '15.57', '15.89', '22.52', '17.61', '5.69', '0.70', '22.10', '8.79', '11.52', '0.15', '3.56', '0.00', '13.85', '7.19', '0.13', '5.58', '2.39']
var consumer_energy_imported_from_grid = ['10.96', '8.69', '13.66', '10.37', '14.63', '8.56', '8.93', '11.33', '7.12', '8.96', '10.99', '8.23', '8.26', '7.66', '7.62', '8.69', '6.19', '8.36', '7.40', '8.77', '9.22', '11.38', '12.45', '15.27', '10.23', '7.95', '13.85', '7.34', '9.47']
var consumer_energy_imported_from_solar = ['4.51', '13.05', '7.50', '7.25', '6.26', '5.86', '7.46', '5.67', '6.06', '4.82', '7.38', '7.25', '4.96', '11.85', '6.20', '6.39', '6.11', '2.98', '6.74', '6.61', '8.58', '2.16', '4.82', '0.44', '6.73', '6.20', '2.09', '3.82', '4.43']
var net_energy = ['1.80', '6.57', '-0.29', '13.39', '5.26', '9.27', '0.20', '6.76', '12.83', '-4.96', '8.69', '15.72', '7.31', '8.24', '14.89', '8.93', '-0.50', '-7.66', '14.70', '0.02', '2.30', '-11.22', '-8.89', '-15.27', '3.62', '-0.76', '-13.72', '-1.75', '-7.08']
var consumer_energy_imported_from_everywhere = ['15.47', '21.74', '21.17', '17.62', '20.89', '14.43', '16.38', '17.00', '13.17', '13.78', '18.37', '15.48', '13.22', '19.50', '13.82', '15.08', '12.30', '11.34', '14.14', '15.37', '17.80', '13.53', '17.27', '15.71', '16.96', '14.15', '15.94', '11.15', '13.90']









Apex.grid = {
  padding: {
    right: 0,
    left: 0
  }
}

Apex.dataLabels = {
  enabled: false
}


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
    data: solar_energy_exported
  }],
  labels: timestamp,
  yaxis: {
    min: 0
  },
  xaxis: {
    type: 'datetime',
    categories: timestamp,
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
    name: 'Net Energy Expored (kWh)',
    data: net_energy
  }],
  labels: timestamp,
  yaxis: {
    min: 0
  },
  xaxis: {
    type: 'datetime',
    categories: timestamp,
  },
  colors: ['#DCE6EC'],
  title: {
    text: lifetime_net_energy + "   ($" + lifetime_net_energy_value + ")",
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
    data: Math.round(lifetime_net_energy/17)
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
    text: Math.round(lifetime_net_energy/17),
    align: 'center',
    margin: 75,
    style: {
      fontSize: '24px',
      cssClass: 'apexcharts-yaxis-title'
    }
  },
  subtitle: {
    text: 'Days Stashed',
    align: 'center',
    margin: 75,
    style: {
      fontSize: '14px',
      cssClass: 'apexcharts-yaxis-title'
    }
  }
}


var spark4 = {
  chart: {
    id: 'sparkline4',
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
    name: 'Dollars Saved',
    data: Math.round(lifetime_energy_imported_from_everywhere*.2938)
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
    text: '$' + Math.round(lifetime_energy_imported_from_everywhere*.2938),
    align: 'center',
    margin: 75,
    style: {
      fontSize: '24px',
      cssClass: 'apexcharts-yaxis-title'
    }
  },
  subtitle: {
    text: 'Dollars Saved',
    align: 'center',
    margin: 75,
    style: {
      fontSize: '14px',
      cssClass: 'apexcharts-yaxis-title'
    }
  }
}

new ApexCharts(document.querySelector("#spark1"), spark1).render();
new ApexCharts(document.querySelector("#spark2"), spark2).render();
new ApexCharts(document.querySelector("#spark3"), spark3).render();
new ApexCharts(document.querySelector("#spark4"), spark4).render();


var optionsArea = {
  title: {
    text: "kWH Produced vs. Used"
  },
  series: [{
  name: 'kWh Produced',
  data: solar_energy_exported
}, {
  name: 'kWh Used',
  data: consumer_energy_imported_from_everywhere
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
  categories: timestamp
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


var optionsEnergyConsumptionChart = {
  title: {
    text: "Energy Consumption (Grid vs. Solar)"
  },
  series: [{
  name: 'From Grid',
  data: consumer_energy_imported_from_grid
}, {
  name: 'From Solar',
  data: consumer_energy_imported_from_solar
}],
  chart: {
  height: 350,
  type: 'area',
  stacked: true,
},
dataLabels: {
  enabled: false
},
stroke: {
  curve: 'smooth'
},
xaxis: {
  type: 'datetime',
  categories: timestamp
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

var energyConsumptionChart = new ApexCharts(document.querySelector("#energyConsumptionChart"), optionsEnergyConsumptionChart);
energyConsumptionChart.render();


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
