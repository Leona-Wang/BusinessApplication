$(document).ready(function () {
    // 獲取供應商列表
    $.ajax({
        url: '/getSupplierList',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var dropdownMenu = $("#supplierDropdown");
            // 處理返回的 JSON 資料
            data.forEach(function (supplier) {
                var item = $('<a class="dropdown-item"></a>')
                    .text(supplier.supplierName) // 顯示供應商名稱
                    .attr("id", supplier.id) // 可選：儲存供應商 ID
                    .on("click", function () {
                        // 當選項被點擊時觸發
                        var selectedSupplier = $(this).text(); // 獲取選中供應商的名稱
                        $("#dropdownMenuButton").text(selectedSupplier); // 更新按鈕文字
                        $("#dropdownMenuButton").data("selected", true); // 標記已選擇
                    });
                dropdownMenu.append(item);
            });
        }
    });

    // 提交表單
    $("#submitMaterialForm").on("submit", function (e) {
        e.preventDefault(); // 阻止表單默認提交行為

        // 獲取表單資料
        const materialName = $("#materialName").val();
        const supplierName = $("#dropdownMenuButton").text();
        const packAmount = $("#packAmount").val();
        const packPrice = $("#packPrice").val();
        const validDay = $("#validDay").val();

        // 檢查下拉選單是否已選擇供應商
        if (!$("#dropdownMenuButton").data("selected")) {
            alert("請選擇供應商！");
            return;
        }

        // 發送資料到後端
        $.ajax({
            url: '/submitMaterial',
            type: 'POST',
            data: {
                materialName: materialName,
                supplierName: supplierName,
                packAmount: packAmount,
                packPrice: packPrice,
                validDay: validDay
            },
            success: function (response) {
                if (response.success) {
                    alert("新增成功！");
                    $("#submitMaterialForm")[0].reset(); // 清空表單
                    $("#dropdownMenuButton").text("請選擇供應商");
                    $("#dropdownMenuButton").data("selected", false); // 重置狀態
                } else {
                    alert("新增失敗：" + response.message);
                    $("#submitMaterialForm")[0].reset(); // 清空表單
                    $("#dropdownMenuButton").text("請選擇供應商");
                    $("#dropdownMenuButton").data("selected", false); // 重置狀態
                }
            },
            error: function (xhr, status, error) {
                alert("發生錯誤：" + error);
                $("#submitMaterialForm")[0].reset(); // 清空表單
                $("#dropdownMenuButton").text("請選擇供應商");
                $("#dropdownMenuButton").data("selected", false); // 重置狀態
            }
        });
    });
});
