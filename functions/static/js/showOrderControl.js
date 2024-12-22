// 從後端獲取資料並生成表格
function getOrderList() {
    $.ajax({
        url: '/getOneTimeOrderList', // 替換成您的 API 路徑
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log("成功取得資料:", data);

            // 獲取表格的 tbody
            const tableBody = $('#oneTimeOrderTable tbody');
            tableBody.empty(); // 清空表格內容

            // 遍歷後端回傳的每一筆資料
            data.forEach(function (order) {
                const orderID=order.id;
                const customerName=order.customerName;
                const customerPhone=order.customerPhone;
                const orderDate=order.orderDate;
                const productNames=order.productNames;
                const amounts=order.amounts;

                // 對於每個產品的第一個原物料，生成產品名稱和原物料的行
                let firstRow = `
                    <tr>
                        <td rowspan="${productNames.length}">${orderID}</td>
                        <td rowspan="${productNames.length}">${customerName}</td>
                        <td rowspan="${productNames.length}">${customerPhone}</td>
                        <td rowspan="${productNames.length}">${orderDate}</td>
                        <td>${productNames[0]}</td>
                        <td>${amounts[0]}</td>
                        <td rowspan="${productNames.length}"><a class="modifyButton btn btn-info btn-icon-split" href="/editOrder/${orderID}/"><span class="icon text-white-50"><i class="fas fa-info-circle"></i></span><span class="text">修改</span></a></td>
                        <td rowspan="${productNames.length}"><a class="deleteButton btn btn-danger btn-icon-split" data-order-id="${orderID}"><span class="icon text-white-50"><i class="fas fa-trash"></i></span><span class="text">刪除</span></a></td>
                    </tr>
                `;
                tableBody.append(firstRow);

                // 對於後續的原物料，僅生成原物料的行
                for (let i = 1; i < productNames.length; i++) {
                    let orderRow = `
                        <tr>
                            <td>${productNames[i]}</td>
                            <td>${amounts[i]}</td>
                        </tr>
                    `;
                    tableBody.append(orderRow);
                }
            });
        },
        error: function (error) {
            console.error("無法取得資料", error);
        }
    });
    $.ajax({
        url: '/getRecurringOrderList', // 替換成您的 API 路徑
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log("成功取得資料:", data);

            // 獲取表格的 tbody
            const tableBody = $('#recurringOrderTable tbody');
            tableBody.empty(); // 清空表格內容

            // 遍歷後端回傳的每一筆資料
            data.forEach(function (order) {
                const orderID=order.id;
                const customerName=order.customerName;
                const customerPhone=order.customerPhone;
                const orderDate=order.orderDate;
                const productNames=order.productNames;
                const amounts=order.amounts;

                // 對於每個產品的第一個原物料，生成產品名稱和原物料的行
                let firstRow = `
                    <tr>
                        <td rowspan="${productNames.length}">${orderID}</td>
                        <td rowspan="${productNames.length}">${customerName}</td>
                        <td rowspan="${productNames.length}">${customerPhone}</td>
                        <td rowspan="${productNames.length}">${orderDate}</td>
                        <td>${productNames[0]}</td>
                        <td>${amounts[0]}</td>
                        <td rowspan="${productNames.length}"><a class="modifyButton btn btn-info btn-icon-split" href="/editOrder/${orderID}/"><span class="icon text-white-50"><i class="fas fa-info-circle"></i></span><span class="text">修改</span></a></td>
                        <td rowspan="${productNames.length}"><a class="deleteButton btn btn-danger btn-icon-split" data-order-id="${orderID}"><span class="icon text-white-50"><i class="fas fa-trash"></i></span><span class="text">刪除</span></a></td>
                    </tr>
                `;
                tableBody.append(firstRow);

                // 對於後續的原物料，僅生成原物料的行
                for (let i = 1; i < productNames.length; i++) {
                    let orderRow = `
                        <tr>
                            <td>${productNames[i]}</td>
                            <td>${amounts[i]}</td>
                        </tr>
                    `;
                    tableBody.append(orderRow);
                }
            });
        },
        error: function (error) {
            console.error("無法取得資料", error);
        }
    });
    $.ajax({
        url: '/getTodayOrderList', // 替換成您的 API 路徑
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log("成功取得資料:", data);

            // 獲取表格的 tbody
            const tableBody = $('#todayOrderTable tbody');
            tableBody.empty(); // 清空表格內容

            // 遍歷後端回傳的每一筆資料
            data.forEach(function (order) {
                const orderID=order.id;
                const customerName=order.customerName;
                const customerPhone=order.customerPhone;
                const orderDate=order.orderDate;
                const productNames=order.productNames;
                const amounts=order.amounts;

                // 對於每個產品的第一個原物料，生成產品名稱和原物料的行
                let firstRow = `
                    <tr>
                        <td rowspan="${productNames.length}">${orderID}</td>
                        <td rowspan="${productNames.length}">${customerName}</td>
                        <td rowspan="${productNames.length}">${customerPhone}</td>
                        <td rowspan="${productNames.length}">${orderDate}</td>
                        <td>${productNames[0]}</td>
                        <td>${amounts[0]}</td>
                        <td rowspan="${productNames.length}"><a class="modifyButton btn btn-info btn-icon-split" href="/editOrder/${orderID}/"><span class="icon text-white-50"><i class="fas fa-info-circle"></i></span><span class="text">修改</span></a></td>
                        <td rowspan="${productNames.length}"><a class="deleteButton btn btn-danger btn-icon-split" data-order-id="${orderID}"><span class="icon text-white-50"><i class="fas fa-trash"></i></span><span class="text">刪除</span></a></td>
                    </tr>
                `;
                tableBody.append(firstRow);

                // 對於後續的原物料，僅生成原物料的行
                for (let i = 1; i < productNames.length; i++) {
                    let orderRow = `
                        <tr>
                            <td>${productNames[i]}</td>
                            <td>${amounts[i]}</td>
                        </tr>
                    `;
                    tableBody.append(orderRow);
                }
            });
        },
        error: function (error) {
            console.error("無法取得資料", error);
        }
    });
}

// 在頁面加載完成後執行
$(document).ready(function () {
    getOrderList();

    $(document).on('click', '.deleteButton', function ()  { 
        const orderID = $(this).data('order-id'); 
        const confirmed = window.confirm('是否確認要刪除訂單？'); 
        if (confirmed) { 
            deleteOrder(orderID); 
        } 
    });
});

function deleteOrder(orderID) {
    $.ajax({
        url: '/deleteOrder',
        type: 'POST',
        data: { id: orderID }, // 傳送 productID
        success: function (response) {
            if (response.success) {
                alert('刪除成功！');
                location.reload();
            } else {
                alert('刪除失敗：' + response.message);
            }
        },
        error: function (xhr, status, error) {
            console.error('發生錯誤:', error);
        },
    });
}


