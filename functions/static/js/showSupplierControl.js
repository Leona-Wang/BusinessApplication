$(document).ready(function() {
    $.ajax({
        url: '/getSupplierList',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            let table = $('#supplierTable');
            let tableBody = $('<tbody>');
            table.append(tableBody);
            console.log(data);
            // 處理返回的 JSON 資料
            // 例如，使用 JavaScript 框架渲染表格
            //let tableBody = $('#supplierTable tbody');
            $.each(data, function(index, supplier) {
                let row = $('<tr></tr>');
                row.append('<td>' + supplier.id + '</td>');
                row.append('<td class="editable">' + supplier.supplierName + '</td>');
                row.append('<td class="editable">' + supplier.supplierPhone + '</td>');
                row.append('<td><a class="modifyButton btn btn-info btn-icon-split"><span class="icon text-white-50"><i class="fas fa-info-circle"></i></span><span class="text">修改</span></a></td>');
                row.append('<td><a class="deleteButton btn btn-danger btn-icon-split"><span class="icon text-white-50"><i class="fas fa-trash"></i></span><span class="text">刪除</span></a></td>');
                tableBody.append(row);
            });
            table.on('click', '.modifyButton', function () {
                let row = $(this).closest('tr'); // 找到按鈕所在的行
                let isEditing = row.data('isEditing'); // 用 data 標記狀態

                if (!isEditing) {
                    // 將文字轉為輸入框
                    row.find('.editable').each(function () {
                        let cell = $(this);
                        let text = cell.text(); // 獲取文字
                        let input = $('<input>').val(text).addClass('form-control'); // 創建輸入框
                        cell.html(input); // 替換內容
                    });
                    $(this).find('.text').text('保存'); // 修改按鈕文字
                    row.data('isEditing', true); // 標記為編輯狀態
                } else {
                    // 保存輸入框中的值
                    row.find('.editable').each(function () {
                        let cell = $(this);
                        let input = cell.find('input');
                        let text = input.val(); // 獲取輸入框值
                        cell.text(text); // 替換為文字
                    });
                    if (!/^\d*$/.test(row.find('td:nth-child(3)').text())) {
                        alert('電話不可為數字以外的內容!');
                        row.find('.editable').each(function () {
                            let cell = $(this);
                            let text = cell.text(); // 獲取文字
                            let input = $('<input>').val(text).addClass('form-control'); // 創建輸入框
                            cell.html(input); // 替換內容
                        });
                        $(this).find('.text').text('保存'); // 修改按鈕文字
                        row.data('isEditing', true);
                        return
                    }
                    $(this).find('.text').text('修改'); // 修改按鈕文字
                    row.data('isEditing', false); // 標記為非編輯狀態

                    
                    $.ajax({
                        url: '/updateSupplier', // Django 後端對應的 URL
                        type: 'POST',           // POST 請求
                        data: {
                            id: row.find('td:first').text(),             // 取得第一欄的 ID
                            supplierName: row.find('td:nth-child(2)').text(), // 第二欄的供應商名稱
                            supplierPhone: row.find('td:nth-child(3)').text() // 第三欄的供應商電話
                        },
                        success: function(response) {
                            if (response.success) {
                                alert('修改成功！');
                                console.log('更新成功:', response.message);
                            } else {
                                alert('修改失敗！');
                                console.warn('更新失敗:', response.message);
                            }
                        },
                        error: function(xhr, status, error) {
                            console.error('請求錯誤:', error);
                        }
                    });
                }
            });
            table.on('click', '.deleteButton', function () {
                const confirmed = window.confirm("是否確認要刪除供應商？");
                if (confirmed){
                    let row = $(this).closest('tr');
                    $.ajax({
                        url: '/deleteSupplier', // Django 後端 API 路徑
                        type: 'POST',          // 使用 POST 請求
                        data: {
                            id:row.find('td:first').text()       // 傳送的資料 ID
                        },
                        success: function (response) {
                            if (response.success) {
                                alert("刪除成功！");
                                // 刪除該行
                                row.remove();
                            } else {
                                alert("刪除失敗：" + response.message);
                            }
                        },
                        error: function (xhr, status, error) {
                            alert("發生錯誤：" + error);
                        }
                    });
                }
                
            });
        },
        error: function(error) {
            console.error('Error fetching data:', error);
        }
    });
    //$('#supplierTable').DataTable();
});


