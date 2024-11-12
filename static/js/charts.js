// Leaderboard Charts
function createLeaderboardCharts(pointsData, countData, amountData) {
    // Points Distribution Chart
    new Chart(document.getElementById('pointsChart'), {
        type: 'bar',
        data: {
            labels: pointsData.map(d => d.user_id),
            datasets: [{
                label: 'Points',
                data: pointsData.map(d => d.points),
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Points Distribution'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Transaction Count Chart
    new Chart(document.getElementById('countChart'), {
        type: 'bar',
        data: {
            labels: countData.map(d => d.user_id),
            datasets: [{
                label: 'Transaction Count',
                data: countData.map(d => d.count),
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Transaction Counts'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Transaction Amount Chart
    new Chart(document.getElementById('amountChart'), {
        type: 'bar',
        data: {
            labels: amountData.map(d => d.user_id),
            datasets: [{
                label: 'Transaction Amount ($)',
                data: amountData.map(d => d.amount),
                backgroundColor: 'rgba(255, 159, 64, 0.6)',
                borderColor: 'rgba(255, 159, 64, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Transaction Amounts'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Transaction History Charts
function createTransactionHistoryCharts(transactionData) {
    // Points Breakdown Pie Chart
    new Chart(document.getElementById('pointsBreakdownChart'), {
        type: 'pie',
        data: {
            labels: [
                'Base Transaction Points',
                'Amount Based Points',
                'Large Transaction Bonus',
                'Frequency Bonus',
                'Streak Bonus'
            ],
            datasets: [{
                data: [
                    transactionData.base_points,
                    transactionData.amount_points,
                    transactionData.large_bonus,
                    transactionData.frequency_bonus,
                    transactionData.streak_bonus
                ],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 159, 64, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 99, 132, 0.6)'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Points Breakdown'
                }
            }
        }
    });

    // Transaction Stats Bar Chart
    new Chart(document.getElementById('statsChart'), {
        type: 'bar',
        data: {
            labels: ['Total Transactions', 'Weekly Streak', 'Daily Frequency'],
            datasets: [{
                label: 'Transaction Statistics',
                data: [
                    transactionData.count,
                    transactionData.weekly_streak,
                    transactionData.transaction_frequency
                ],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 159, 64, 0.6)'
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Transaction Statistics'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
