// 從後端獲取資料並生成表格
function getIngredientList() {
    $.ajax({
        url: '/getBOMList', // 替換成您的 API 路徑
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log("成功取得資料:", data);

            // 獲取表格的 tbody
            const tableBody = $('#BOMTable tbody');
            tableBody.empty(); // 清空表格內容

            // 遍歷後端回傳的每一筆資料
            data.forEach(function (bom) {
                const productID = bom.id;
                const productName=bom.productName;
                const productPrice=bom.productPrice;
                const materialNames=bom.materialNames;
                const units=bom.units;

                // 對於每個產品的第一個原物料，生成產品名稱和原物料的行
                let firstRow = `
                    <tr>
                        <td rowspan="${materialNames.length}">${productID}</td>
                        <td rowspan="${materialNames.length}">${productName}</td>
                        <td rowspan="${materialNames.length}">${productPrice}</td>
                        <td>${materialNames[0]}</td>
                        <td>${units[0]}</td>
                        <td rowspan="${materialNames.length}"><a class="modifyButton btn btn-info btn-icon-split" href="/edit/${productID}/"><span class="icon text-white-50"><i class="fas fa-info-circle"></i></span><span class="text">修改</span></a></td>
                        <td rowspan="${materialNames.length}"><a class="deleteButton btn btn-danger btn-icon-split" data-product-id="${productID}"><span class="icon text-white-50"><i class="fas fa-trash"></i></span><span class="text">刪除</span></a></td>
                    </tr>
                `;
                tableBody.append(firstRow);

                // 對於後續的原物料，僅生成原物料的行
                for (let i = 1; i < materialNames.length; i++) {
                    let materialRow = `
                        <tr>
                            <td>${materialNames[i]}</td>
                            <td>${units[i]}</td>
                        </tr>
                    `;
                    tableBody.append(materialRow);
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
    getIngredientList();

    $('#BOMTable').on('click', '.deleteButton', function () {

        // 從按鈕的 data-product-id 屬性取得 productID
        const productID = $(this).data('product-id');
        const confirmed = window.confirm('是否確認要刪除產品？');
        if (confirmed) {
            deleteProduct(productID);
        }
    });
});

function deleteProduct(productID) {
    $.ajax({
        url: '/deleteProduct',
        type: 'POST',
        data: { id: productID }, // 傳送 productID
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
