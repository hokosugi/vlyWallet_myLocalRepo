// Leaderboard Charts
function createLeaderboardCharts(pointsData, countData, amountData) {
    // Points Distribution Chart
    new Chart(document.getElementById('pointsChart'), {
        type: 'bar',
        data: {
            labels: pointsData.map(d => d.user_id),
            datasets: [{
                label: gettext('Points'),
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
                    text: gettext('Points Distribution')
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
                label: gettext('Transaction Count'),
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
                    text: gettext('Transaction Counts')
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
                label: gettext('Transaction Amount ($)'),
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
                    text: gettext('Transaction Amounts')
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
                gettext('Base Points'),
                gettext('Amount Points'),
                gettext('Large Transaction Bonus'),
                gettext('Frequency Bonus'),
                gettext('Streak Bonus')
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
                    text: gettext('Points Breakdown')
                }
            }
        }
    });

    // Transaction Stats Bar Chart
    new Chart(document.getElementById('statsChart'), {
        type: 'bar',
        data: {
            labels: [
                gettext('Total Transactions'),
                gettext('Weekly Streak'),
                gettext('Daily Frequency')
            ],
            datasets: [{
                label: gettext('Transaction Statistics'),
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
                    text: gettext('Transaction Statistics')
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

// Add gettext function for translations
function gettext(text) {
    // This function would normally be provided by a JavaScript i18n library
    // For now, we'll use a simple object to store translations
    const translations = {
        'Points': 'ポイント',
        'Points Distribution': 'ポイント分布',
        'Transaction Count': '取引回数',
        'Transaction Counts': '取引回数',
        'Transaction Amount ($)': '取引額 ($)',
        'Transaction Amounts': '取引金額',
        'Base Points': '基本ポイント',
        'Amount Points': '金額ポイント',
        'Large Transaction Bonus': '大口取引ボーナス',
        'Frequency Bonus': '頻度ボーナス',
        'Streak Bonus': '連続ボーナス',
        'Points Breakdown': 'ポイント内訳',
        'Total Transactions': '総取引数',
        'Weekly Streak': '週連続',
        'Daily Frequency': '1日あたりの頻度',
        'Transaction Statistics': '取引統計'
    };
    return translations[text] || text;
}
