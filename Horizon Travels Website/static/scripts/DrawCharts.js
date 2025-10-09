// Author: Aaron Antal-Bento ID: 23013693
// Declare a global variable to store the chart instance
var journeySalesChart = null;
function drawJourneySales() {
    // Create a new XMLHttpRequest object
    var xhttp = new XMLHttpRequest();

    // Show the chart holder
    document.getElementById('journeySalesChartHolder').style.display = 'block';

    // Get the selected sales type from the selector (default is "alltime")
    var salesType = document.getElementById('salesSelector').value;

    // Define the function that is called when the AJAX request is complete
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            // Parse the received response into a JSON array
            const responseData = JSON.parse(xhttp.responseText);

            // Labels and data from the response
            const labels = responseData[0];
            const standardSeats = responseData[1]; // Standard seats data
            const firstClassSeats = responseData[2]; // First class seats data
            const cancelledSeats = responseData[3];

            // Define the data configuration
            const data = {
                labels: labels,
                datasets: [
                    {
                        label: 'Standard Seats',
                        data: standardSeats,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        backgroundColor: 'rgba(75, 192, 192, 0.5)',
                        borderWidth: 1,
                    },
                    {
                        label: 'First Class Seats',
                        data: firstClassSeats,
                        borderColor: 'rgb(99, 109, 255)',
                        backgroundColor: 'rgba(99, 107, 255, 0.5)',
                        borderWidth: 1,
                    },
                    {
                        label: 'Cancelled Seats',
                        data: cancelledSeats,
                        borderColor: 'rgba(255, 99, 132, 1)',
                        backgroundColor: 'rgba(255, 99, 132, 0.5)',
                        borderWidth: 1,
                    }
                ]
            };

            // Define the chart configuration
            const config = {
                type: 'horizontalBar', // Horizontal bar chart (Chart.js version 2.x)
                data: data,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        xAxes: [{
                            stacked: true, // Stacks the data horizontally
                            ticks: {
                                stepSize: 5,
                                autoSkip: true, // Enables automatic skipping
                                autoSkipPadding: 30, // Padding between the labels (in pixels)
                            }
                        }],
                        yAxes: [{
                            stacked: true, // Stacks the data vertically
                        }]
                    },
                    legend: { // Legend settings
                        position: 'top',
                    },
                    title: { // Chart title including the sales type
                        display: true,
                        text: 'Journey Seats Overview (Stacked) - ' +
                            salesType.charAt(0).toUpperCase() + salesType.slice(1) + ' Sales'
                    }
                }
            };

            // Get the canvas context
            const ctx = document.getElementById("journeySalesChart").getContext("2d");

            // If a chart already exists, destroy it before creating a new one
            if (journeySalesChart) {
                journeySalesChart.destroy();
            }

            // Create a new Chart instance and assign it to journeySalesChart
            journeySalesChart = new Chart(ctx, config);
        }
    };

    // Send the AJAX request to the endpoint with the sales type as a query parameter
    xhttp.open("GET", "/getjourneysales/?salesType=" + salesType, true);
    xhttp.send();
}

var journeyRevenueChart = null;
function drawJourneyRevenue() {
    // Create a new XMLHttpRequest object
    var xhttp = new XMLHttpRequest();

    // Show the chart holder
    document.getElementById('journeyRevenueChartHolder').style.display = 'block';

    // Get the selected sales type from the selector (default is "alltime")
    var salesType = document.getElementById('salesSelector2').value;

    // Define the function that is called when the AJAX request is complete
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            // Parse the received response into a JSON array
            const responseData = JSON.parse(xhttp.responseText);

            // Labels and data from the response
            const labels = responseData[0];
            const amountMade = responseData[1];
            const amountCancelled = responseData[2];

            // Define the data configuration
            const data = {
                labels: labels,
                datasets: [
                    {
                        label: 'Revenue made',
                        data: amountMade,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        backgroundColor: 'rgba(75, 192, 192, 0.5)',
                        borderWidth: 1,
                    },
                    {
                        label: 'Revenue refunded',
                        data: amountCancelled,
                        borderColor: 'rgba(255, 99, 132, 1)',
                        backgroundColor: 'rgba(255, 99, 132, 0.5)',
                        borderWidth: 1,
                    }
                ]
            };

            // Define the chart configuration
            const config = {
                type: 'horizontalBar',
                data: data,
                options: {
                    responsive: true,
                    maintainAspectRatio: false, // Allow dynamic resizing
                    scales: {
                        xAxes: [{
                            stacked: true,
                            ticks: {
                                stepSize: 100,
                                autoSkip: true, // Enables automatic skipping
                                autoSkipPadding: 30, // Padding between the labels (in pixels)
                                callback: function (value) {
                                    return '£' + value.toLocaleString(); // Prepend the £ sign to each label
                                }
                            }
                        }],
                        yAxes: [{
                            stacked: true
                        }]
                    },
                    tooltips: {
                        callbacks: {
                            label: function (tooltipItem, data) {
                                return '£' + tooltipItem.xLabel.toLocaleString();
                            }
                        }
                    },
                    legend: { // Legend settings
                        position: 'top',
                    },
                    title: { // Chart title including the sales type
                        display: true,
                        text: 'Journey Revenue Overview (Stacked) - ' +
                            salesType.charAt(0).toUpperCase() + salesType.slice(1) + ' Sales'
                    }
                }
            };

            // Get the canvas context
            const ctx = document.getElementById("journeyRevenueChart").getContext("2d");

            // If a chart already exists, destroy it before creating a new one
            if (journeyRevenueChart) {
                journeyRevenueChart.destroy();
            }

            journeyRevenueChart = new Chart(ctx, config);
            document.getElementById('journeyRevenueChart').scrollIntoView({ behavior: 'smooth', block: 'top' });
        }
    };

    // Send the AJAX request to the endpoint with the sales type as a query parameter
    xhttp.open("GET", "/getjourneyrevenue/?salesType=" + salesType, true);
    xhttp.send();
}

var singleJourneySalesChart = null;
function drawSingleJourneySales() {
    // Create a new XMLHttpRequest object
    var xhttp = new XMLHttpRequest();

    // Show the chart holder
    document.getElementById('singleJourneySalesChartHolder').style.display = 'block';
    var journey1ID = document.getElementById('idSelector').value;
    var journey2ID = document.getElementById('idSelector2').value;
    if (!journey2ID && !journey1ID) {
        document.getElementById('singleJourneySalesChartHolder').style.display = 'none'; return;
    }


    // Define the function that is called when the AJAX request is complete
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            // Parse the received response into a JSON array
            const responseData = JSON.parse(xhttp.responseText);

            // Define the data configuration
            const data = responseData;
            const today = new Date();

            // Define the chart configuration
            const config = {
                type: 'line',
                data: data,
                options: {
                    responsive: true,
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true,
                                callback: function (value) {
                                    return '£' + value.toLocaleString(); // Prepend the £ sign to each label
                                }
                            }
                        }],
                    },
                    tooltips: {
                        callbacks: {
                            label: function (tooltipItem) {
                                return '£' + tooltipItem.yLabel.toLocaleString();
                            }
                        }
                    },
                    annotation: {
                        // Place annotation definitions here
                        annotations: [{
                            type: 'line',
                            mode: 'vertical',
                            scaleID: 'x-axis-0',
                            // Use the same string as one of your x-axis labels
                            value: 'Today',
                            borderColor: 'lightgreen',
                            borderWidth: 2,
                            label: {
                                enabled: true,
                                position: "top",
                                xAdjust: 22,
                                fontColor: '#000',
                                backgroundColor: 'rgba(0, 0, 0, 0.05)',
                                content: 'Today'
                            }
                        }]
                    },
                    legend: { // Legend settings
                        position: 'top',
                    },
                    title: { // Chart title including the sales type
                        display: true,
                        text: 'Journey Sales Comparison - '
                    },

                },
            };

            // Get the canvas context
            const ctx = document.getElementById("singleJourneySalesChart").getContext("2d");

            // If a chart already exists, destroy it before creating a new one
            if (singleJourneySalesChart) {
                singleJourneySalesChart.destroy();
            }

            // Create a new Chart instance and assign it to journeySalesChart
            singleJourneySalesChart = new Chart(ctx, config);
            document.getElementById('singleJourneySalesChart').scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    };

    // Send the AJAX request to the endpoint with the sales type as a query parameter
    xhttp.open("GET", "/getsinglejourneysales/?journey1ID=" + journey1ID + "&journey2ID=" + journey2ID, true);
    xhttp.send();
}

var companyPieChart = null;
function companyData() {
    // Create a new XMLHttpRequest object
    var xhttp = new XMLHttpRequest();

    // Show the chart and data container
    document.getElementById('TIContent').style.display = 'flex';

    // When the AJAX request returns...
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const responseData = JSON.parse(this.responseText);

            const companyNames = responseData[0];
            const totalRevenues = responseData[1];
            const totalSeatsBooked = responseData[2];
            const firstClassSeats = responseData[3];
            const cancelledSeats = responseData[4];
            const journeysRunning = responseData[5];
            const citiesInNetwork = responseData[6];
            const daysInService = responseData[7];

            // Update the data fields in the HTML for each company.
            // We assume that the order of .companyDataHolder elements corresponds to companyNames.
            const companyHolders = document.getElementsByClassName('companyDataHolder');
            for (let i = 0; i < companyHolders.length; i++) {
                // Find the container that holds the actual data values
                let cdData = companyHolders[i].getElementsByClassName('CDData')[0];
                if (cdData) {
                    let pElements = cdData.getElementsByTagName('p');

                    // Format total revenue with a currency symbol and locale formatting.
                    pElements[0].textContent = "£" + Number(totalRevenues[i]).toLocaleString();

                    // Update remaining fields with the corresponding data.
                    pElements[1].textContent = totalSeatsBooked[i];
                    pElements[2].textContent = firstClassSeats[i] + "%";
                    pElements[3].textContent = cancelledSeats[i];
                    pElements[4].textContent = journeysRunning[i];
                    pElements[5].textContent = citiesInNetwork[i];

                    // For days in service, check if the data is an array. If so, join its items with commas.
                    if (Array.isArray(daysInService[i])) {
                        pElements[6].textContent = daysInService[i].join(", ");
                    } else {
                        pElements[6].textContent = daysInService[i];
                    }
                }
            }

            // Create a pie chart for total revenue per company.
            const pieData = {
                labels: companyNames,
                datasets: [{
                    data: totalRevenues,
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.5)',  // Color for first company
                        'rgba(99, 109, 255, 0.5)'   // Color for second company
                    ],
                    borderColor: [
                        'rgba(75, 192, 192, 1)',
                        'rgb(99, 109, 255)'
                    ],
                    borderWidth: 1
                }]
            };

            const config = {
                type: 'pie',
                data: pieData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    legend: {
                        position: 'top'
                    },
                    tooltips: {
                        callbacks: {
                            label: function(tooltipItem, data) {
                                var label = data.labels[tooltipItem.index] || '';
                                var value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                                return label + ': £' + parseFloat(value).toLocaleString();
                            }
                        }
                    },
                    title: {
                        display: true,
                        text: 'Total Revenue per Company'
                    }
                }
            };

            // Get the canvas context for the pie chart
            const ctx = document.getElementById("companyPieChart").getContext("2d");

            // Destroy any previous chart instance before creating a new one.
            if (companyPieChart) {
                companyPieChart.destroy();
            }

            // Create a new Chart instance.
            companyPieChart = new Chart(ctx, config);
            document.getElementById('TIContent').scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    };

    // Send the AJAX request. The endpoint should provide the data in the format described above.
    xhttp.open("GET", "/getcompanydata/", true);
    xhttp.send();
}