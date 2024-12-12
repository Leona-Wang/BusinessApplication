$(document).ready(function () {
    // 初始化獲取表格數據
    loadMaterialTable();

    // 綁定修改按鈕事件
    $('#materialTable').on('click', '.modifyButton', function () {
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
                } else if (cell.hasClass('supplierCell')) {
                    // 獲取下拉選單
                    setupSupplierDropdown(cell);
                } else {
                    let text = cell.text();
                    let input = $('<input>').val(text).addClass('form-control');
                    cell.html(input);
                }
            });

            $(this).find('.text').text('保存');
            row.data('isEditing', true); // 標記為編輯狀態
        } else {
            // 保存數據並發送到後端
            saveMaterialData(row, $(this));
        }
    });

    // 綁定刪除按鈕事件
    $('#materialTable').on('click', '.deleteButton', function () {
        let row = $(this).closest('tr');
        const confirmed = window.confirm('是否確認要刪除原物料？');
        if (confirmed) {
            deleteMaterial(row);
        }
    });
});

// 獲取原物料數據的函數
function loadMaterialTable() {
    $.ajax({
        url: '/getMaterialList',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let table = $('#materialTable');
            let tableBody = $('<tbody>');
            table.append(tableBody);

            $.each(data, function (index, material) {
                let row = $('<tr></tr>');
                row.append('<td>' + material.id + '</td>');
                row.append('<td class="editable">' + material.materialName + '</td>');
                row.append('<td class="editable numberCell">' + material.packPrice + '</td>');
                row.append('<td class="editable numberCell">' + material.packAmount + '</td>');
                row.append('<td class="editable numberCell">' + material.validDay + '</td>');
                row.append('<td class="editable supplierCell">' + material.supplierName + '</td>');
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
function setupSupplierDropdown(cell) {
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
        url: '/getSupplierList',
        type: 'GET',
        dataType: 'json',
        success: function (suppliers) {
            let dropdownMenu = dropdown.find('.dropdown-menu');
            suppliers.forEach(function (supplier) {
                let item = $('<a class="dropdown-item"></a>')
                    .text(supplier.supplierName)
                    .on('click', function () {
                        dropdown.find('button').text(supplier.supplierName);
                        dropdown.data('selectedValue', supplier.supplierName);
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
function saveMaterialData(row, button) {
    row.find('.editable').each(function () {
        let cell = $(this);

        if (cell.hasClass('supplierCell')) {
            let dropdown = cell.find('.dropdown');
            let selectedValue = dropdown.data('selectedValue') || dropdown.find('button').text();
            cell.text(selectedValue);
        } else {
            let input = cell.find('input');
            let text = input.val();
            cell.text(text);
        }
    });

    // 發送更新請求
    $.ajax({
        url: '/updateMaterial',
        type: 'POST',
        data: {
            id: row.find('td:first').text(),
            materialName: row.find('td:nth-child(2)').text(),
            packPrice: row.find('td:nth-child(3)').text(),
            packAmount: row.find('td:nth-child(4)').text(),
            validDay: row.find('td:nth-child(5)').text(),
            supplierName: row.find('td:nth-child(6)').text(),
        },
        success: function (response) {
            if (response.success) {
                alert('修改成功！');
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
function deleteMaterial(row) {
    $.ajax({
        url: '/deleteMaterial',
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
