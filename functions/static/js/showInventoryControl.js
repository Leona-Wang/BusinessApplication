
$(document).ready(function () {
    // 初始化獲取表格數據
    loadInventoryTable();

    // 綁定修改按鈕事件
    $('#inventoryTable').on('click', '.modifyButton', function () {
        let row = $(this).closest('tr'); // 找到按鈕所在的行
        let isEditing = row.data('isEditing'); // 用 data 標記狀態

        if (!isEditing) {
            // 進入編輯模式
            row.find('.editable').each(function () {
                let cell = $(this);

                if (cell.hasClass('numberCell')) {
                    let currentValue = cell.text();
                    let numberInput = $(
                        `<div class="input-group">
                            <input type="number" class="form-control bg-light border-1 small" value="${currentValue}" required>
                        </div>`
                    );
                    cell.html(numberInput);
                } else if (cell.hasClass('dropdownCell')) {
                    // 獲取下拉選單
                    setupMaterialDropdown(cell);
                } else {
                    let currentValue = cell.text();
                    let numberInput = $(
                        `<div class="input-group" id="importDay">
                            <input type="date" class="form-control bg-light border-1 small" id="importDate" name="importDate" value="${currentValue}" required>
                        </div>`
                    );
                    cell.html(numberInput);
                    const today = new Date();
                    const yyyy = today.getFullYear();
                    const mm = String(today.getMonth() + 1).padStart(2, '0'); // 月份補0
                    const dd = String(today.getDate()).padStart(2, '0'); // 日期補0

                    const minDate = `${yyyy}-${mm}-${dd}`; // 格式化為 YYYY-MM-DD

                    // 設置 input 的最小日期
                    const dateInput = document.getElementById('importDate');
                    dateInput.min = minDate;
                    dateInput.value = minDate; // 可選：默認值設為當天                    
                    
                }
            });

            $(this).find('.text').text('保存');
            row.data('isEditing', true); // 標記為編輯狀態
        } else {
            // 保存數據並發送到後端
            saveInventoryData(row, $(this));
        }
    });

    // 綁定刪除按鈕事件
    $('#inventoryTable').on('click', '.deleteButton', function () {
        let row = $(this).closest('tr');
        const confirmed = window.confirm('是否確認要刪除原物料？');
        if (confirmed) {
            deleteInventory(row);
        }
    });
});

// 獲取原物料數據的函數
function loadInventoryTable() {
    $.ajax({
        url: '/getInventoryList',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let table = $('#inventoryTable');
            let tableBody = $('<tbody>');
            table.append(tableBody);

            $.each(data, function (index, inventory) {
                let row = $('<tr></tr>');
                row.append('<td>' + inventory.id + '</td>');
                row.append('<td class="editable dropdownCell">' + inventory.materialName + '</td>');
                row.append('<td class="editable numberCell">' + inventory.importPack + '</td>');
                row.append('<td>' + inventory.importAmount + '</td>');
                row.append('<td class="editable dateCell">' + inventory.importDate + '</td>');
                row.append('<td>' + inventory.expiredDate + '</td>');
                row.append('<td><a class="modifyButton btn btn-info btn-icon-split"><span class="icon text-white-50"><i class="fas fa-info-circle"></i></span><span class="text">修改</span></a></td>');
                row.append('<td><a class="deleteButton btn btn-danger btn-icon-split"><span class="icon text-white-50"><i class="fas fa-trash"></i></span><span class="text">刪除</span></a></td>');
                tableBody.append(row);
            });
        },
        error: function (error) {
            console.error('Error fetching data:', error);
        },
    });
}

// 設置供應商下拉選單
function setupMaterialDropdown(cell) {
    let currentValue = cell.text();
    let dropdown = $(`
        <div class="dropdown no-arrow mb-4">
            <button class="col-lg-12 btn btn-secondary dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                ${currentValue}
            </button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton"></div>
        </div>
    `);

    // 獲取供應商列表
    $.ajax({
        url: '/getMaterialList',
        type: 'GET',
        dataType: 'json',
        success: function (materials) {
            let dropdownMenu = dropdown.find('.dropdown-menu');
            materials.forEach(function (material) {
                let item = $('<a class="dropdown-item"></a>')
                    .text(material.materialName)
                    .on('click', function () {
                        dropdown.find('button').text(material.materialName);
                        dropdown.data('selectedValue', material.materialName);
                    });
                dropdownMenu.append(item);
            });
        },
        error: function (xhr, status, error) {
            alert('無法加載供應商列表：' + error);
        },
    });

    cell.html(dropdown);
}

// 保存修改數據的函數
function saveInventoryData(row, button) {
    row.find('.editable').each(function () {
        let cell = $(this);

        if (cell.hasClass('dropdownCell')) {
            let dropdown = cell.find('.dropdown');
            let selectedValue = dropdown.data('selectedValue') || dropdown.find('button').text();
            cell.text(selectedValue);
        }
        else {
            let input = cell.find('input');
            let text = input.val();
            cell.text(text);
        }
    });
    let formData={id: row.find('td:first').text(),
        materialName: row.find('td:nth-child(2)').text(),
        importPack: row.find('td:nth-child(3)').text(),
        importDate: row.find('td:nth-child(5)').text(),};
    alert(JSON.stringify(formData))

    // 發送更新請求
    $.ajax({
        url: '/updateInventory',
        type: 'POST',
        contentType: 'application/json', // 明確指定為 JSON 格式
        data: JSON.stringify({
            id: row.find('td:first').text(),
            materialName: row.find('td:nth-child(2)').text(),
            importPack: row.find('td:nth-child(3)').text(),
            importDate: row.find('td:nth-child(5)').text(),
        }),
        success: function (response) {
            if (response.success) {
                alert('修改成功！');
                location.reload();
            } else {
                alert('修改失敗：' + response.message);
            }
        },
        error: function (xhr, status, error) {
            console.error('請求錯誤:', error);
        },
    });

    button.find('.text').text('修改');
    row.data('isEditing', false);
}

// 刪除原物料的函數
function deleteInventory(row) {
    $.ajax({
        url: '/deleteInventory',
        type: 'POST',
        data: {
            id: row.find('td:first').text(),
        },
        success: function (response) {
            if (response.success) {
                alert('刪除成功！');
                row.remove();
            } else {
                alert('刪除失敗：' + response.message);
            }
        },
        error: function (xhr, status, error) {
            console.error('發生錯誤:', error);
        },
    });
}
