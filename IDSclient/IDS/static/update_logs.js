function formated_date(time, type) {
    const d = new Date(time),
    year = new Intl.DateTimeFormat('en', { year: 'numeric' }).format(d),
    month = new Intl.DateTimeFormat('en', { month: 'numeric' }).format(d),
    day = new Intl.DateTimeFormat('en', { day: 'numeric' }).format(d),
    hour = new Intl.DateTimeFormat('en', { hour: 'numeric', hour12: false }).format(d),
    minute = new Intl.DateTimeFormat('en', { minute: 'numeric' }).format(d),
    second = new Intl.DateTimeFormat('en', { second: 'numeric' }).format(d)

    if (type == "long")
        return `${year}-${month}-${day} ${hour}:${minute}:${second}`
    
    else
        return `${hour}:${minute}`
}

//call upd_logs from views.py and update log list and graph
function get_next(len_log_list) {
    $.ajax({
        type: 'get',
        url: 'update_logs/',
        data: {'last_log_id': len_log_list},
        success: function (response) {
            chart.data.labels.push(response[2])
            if (chart.data.labels.length == 10)
                chart.data.labels.splice(0, 1)

            chart.data.datasets.forEach((dataset) => {
                dataset.data.push(response[1])
                if (response[1] < 20) {
                    dataset.borderColor = '#31850a'
                    dataset.backgroundColor = 'rgba(49, 133, 10, 0.2)'
                }
                else if (response[1] >= 20 && response[1] < 40) {
                    dataset.borderColor = '#FCD74E'
                    dataset.backgroundColor = 'rgba(252, 215, 78, 0.2)'
                }
                else {
                    dataset.borderColor = '#9c3113'
                    dataset.backgroundColor = 'rgba(156, 49, 19, 0.2)'
                }

                if (dataset.data.length == 10)
                    dataset.data.splice(0, 1)
            });

            chart.update()

            if (response[0]) {
                response[0].forEach(log => 
                    $( 'table' ).append( `<tr>
                                            <th class="log_id">${log.id}</th>
                                            <th class="log_text">${log.message}</th>
                                            <th class="log_time">${formated_date(log.timestamp, "short")}
                                                <span class="tooltiptext">${formated_date(log.timestamp, "long")}</span>
                                            </th>
                                          </tr>` ))
            }
            setTimeout(function(){ get_next(len_log_list + response[0].length) }, 3000)
        },
        error: function (response) {
            setTimeout(function(){ get_next(len_log_list) }, 3000)
        }
    })
}

var ctx = document.getElementById('log_chart').getContext('2d'),

//graph
chart = new Chart(ctx, {
    type: 'line',

    data: {
        labels: [],
        datasets: [{
            label: 'Danger',
            backgroundColor: 'rgba(255, 255, 255, 0)',
            borderColor: '#66cccc',
            data: []
        }]
    },

    options: {
        responsive:true,
        maintainAspectRatio: false,
        legend: {
            display: false
        },

        scales: {
            yAxes: [{
                ticks: {
                    suggestedMin: 0
                }
            }]
        }
    }
})

get_next(parseInt(document.getElementById("update_logs").getAttribute("last_id"), 10))

