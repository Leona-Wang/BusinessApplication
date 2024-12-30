$(document).ready(function () {
    loadImportantTable();
    loadNormalTable();
    loadDangerTable();
});

function loadImportantTable() {
    $.ajax({
        url: '/getImportantList',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let table = $('#importantTable');
            let tableBody = $('<tbody>');
            table.append(tableBody);

            $.each(data, function (index, important) {
                let row = $('<tr></tr>');
                row.append('<td>' + important.customerName + '</td>');
                row.append('<td>' + important.customerPhone + '</td>');
                tableBody.append(row);
            });
        },
        error: function (error) {
            console.error('Error fetching data:', error);
        },
    });
}
function loadNormalTable() {
    $.ajax({
        url: '/getNormalList',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let table = $('#normalTable');
            let tableBody = $('<tbody>');
            table.append(tableBody);

            $.each(data, function (index, normal) {
                let row = $('<tr></tr>');
                row.append('<td>' + normal.customerName + '</td>');
                row.append('<td>' + normal.customerPhone + '</td>');
                tableBody.append(row);
            });
        },
        error: function (error) {
            console.error('Error fetching data:', error);
        },
    });
}
function loadDangerTable() {
    $.ajax({
        url: '/getDangerList',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let table = $('#dangerTable');
            let tableBody = $('<tbody>');
            table.append(tableBody);

            $.each(data, function (index, danger) {
                let row = $('<tr></tr>');
                row.append('<td>' + danger.customerName + '</td>');
                row.append('<td>' + danger.customerPhone + '</td>');
                tableBody.append(row);
            });
        },
        error: function (error) {
            console.error('Error fetching data:', error);
        },
    });
}