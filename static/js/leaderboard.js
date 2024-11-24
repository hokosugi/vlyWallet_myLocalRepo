// Real-time updates handling
let eventSource;

function setupEventSource() {
    eventSource = new EventSource("/stream");
    
    eventSource.addEventListener('transaction_update', function(event) {
        const data = JSON.parse(event.data);
        updateLeaderboardData(data);
    });

    eventSource.onerror = function(error) {
        console.error("EventSource failed:", error);
        eventSource.close();
        // Attempt to reconnect after 5 seconds
        setTimeout(setupEventSource, 5000);
    };
}

function updateLeaderboardData(data) {
    // Update points leaderboard
    updateLeaderboardEntry('points', data.user_id, data.points);
    
    // Update transaction count leaderboard
    updateLeaderboardEntry('count', data.user_id, data.count);
    
    // Update transaction amount leaderboard
    updateLeaderboardEntry('amount', data.user_id, data.amount);
    
    // Refresh charts
    // const pointsData = getLeaderboardData('points');
    const countData = getLeaderboardData('count');
    // const amountData = getLeaderboardData('amount');
    createLeaderboardCharts(countData);
}

function updateLeaderboardEntry(type, userId, value) {
    const table = document.querySelector(`#${type}Chart`).closest('.card').querySelector('table tbody');
    let found = false;
    
    // Update existing entry
    for (let row of table.rows) {
        if (row.cells[1].textContent === userId) {
            row.cells[2].textContent = type === 'amount' ? `$${value.toFixed(2)}` : value;
            found = true;
            break;
        }
    }
    
    // Add new entry if not found
    if (!found && table.rows.length < 10) {
        const newRow = table.insertRow();
        newRow.insertCell(0).textContent = table.rows.length + 1;
        newRow.insertCell(1).textContent = userId;
        newRow.insertCell(2).textContent = type === 'amount' ? `$${value.toFixed(2)}` : value;
    }
    
    // Sort table
    sortLeaderboardTable(table, 2, type === 'amount');
}

function sortLeaderboardTable(table, column, isAmount) {
    const rows = Array.from(table.rows);
    rows.sort((a, b) => {
        const aVal = isAmount ? 
            parseFloat(a.cells[column].textContent.replace('$', '')) :
            parseInt(a.cells[column].textContent);
        const bVal = isAmount ?
            parseFloat(b.cells[column].textContent.replace('$', '')) :
            parseInt(b.cells[column].textContent);
        return bVal - aVal;
    });
    
    // Update rank numbers and reorder rows
    rows.forEach((row, index) => {
        row.cells[0].textContent = index + 1;
        table.appendChild(row);
    });
}

function getLeaderboardData(type) {
    const table = document.querySelector(`#${type}Chart`).closest('.card').querySelector('table tbody');
    return Array.from(table.rows).map(row => ({
        user_id: row.cells[1].textContent,
        [type]: type === 'amount' ? 
            parseFloat(row.cells[2].textContent.replace('$', '')) :
            parseInt(row.cells[2].textContent)
    }));
}

// Leaderboard data management
function updateLeaderboard() {
    // Refresh the page to get the latest data
    location.reload();
}

// Refresh leaderboard data every hour
setInterval(updateLeaderboard, 3600000);

// Initialize real-time updates when the page loads
document.addEventListener('DOMContentLoaded', function() {
    setupEventSource();
});