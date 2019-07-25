class PensionsController {
    constructor (yearData, selectedYear, selectedFund, chartHelper) {
        this.yearData = yearData
        this.selectedYear = selectedYear
        this.selectedFund = selectedFund
        this.chartHelper = chartHelper
    }
    selectYear (year) {
        this.selectedYear = year

        var data = this.yearData[year]

        this.chartHelper.makeBarChart(data.aggregate_funding);

        return this.yearData[year]
    }
    selectFund (fund) {
        this.selectedFund = fund

        var data = this.selectYear(this.selectedYear)['data_by_fund'][fund]

        $('#fundDropdownMenuButton').text(fund);

        this.chartHelper.makePieChart(data.aggregate_funding);
        this.chartHelper.makeBarChart(data.amortization_cost);

        $('#funding-level').text(data.funding_level + '%');

        return data
    }
}

class ChartHelper {
    constructor () {
        Highcharts.setOptions({
            lang: {
              thousandsSep: ',',
            },
            colors: ['#01406c', '#dc3545'],
        });
    }
    makeBarChart (data) {
        Highcharts.chart(data.container, {
            plotOptions: {
                bar: {
                    dataLabels: {
                        enabled: true,
                        format: data.label_format,
                    },
                    enableMouseTracking: false,
                },
                series: {
                    stacking: data.stacked ? 'normal' : undefined,
                },
            },
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'bar',
            },
            title: {
                text: data.name,
                align: data.name_align ? data.name_align : 'center',
            },
            xAxis: {
                categories: data.x_axis_categories,
                title: {
                    text: null
                },
                labels: {
                    style: {
                        fontSize: '15px',
                    }
                },
            },
            yAxis: {
                min: 0,
                max: data.stacked ? (data.funded.data[0] + data.unfunded.data[0]) : null,
                endOnTick: false,
                title: {
                    text: data.axis_label,
                },
            },
            legend: {
                verticalAlign: 'top',
            },
            tooltip: {
                pointFormat: '{series.name}: <b>' + data.label_format + '</b>'
            },
            series: [data.funded, data.unfunded],
        });
    }
    makePieChart (data) {
        Highcharts.chart(data.container, {
            chart: {
                type: 'pie'
            },
            title: {
                text: data.name,
                align: 'left',
            },
            tooltip: {
                enabled: false,
            },
            legend: {
                enabled: false,
            },
            plotOptions: {
                pie: {
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>:<br />' + data.label_format,
                    },
                    enableMouseTracking: false,
                }
            },
            series: [data.series_data],
        });
    }
}

export { PensionsController, ChartHelper };
