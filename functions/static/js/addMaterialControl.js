$(document).ready(function () {
    console.log("Document is ready!");

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
                    .text(supplier.supplierName)  // 顯示供應商名稱
                    .attr("id", supplier.id)  // 儲存供應商 ID
                    .on("click", function () {
                        // 當選項被點擊時觸發
                        var selectedSupplier = $(this).text();  // 獲取選中供應商的名稱
                        $("#dropdownMenuButton").text(selectedSupplier);  // 更新按鈕文字
                        $("#dropdownMenuButton").data("selected", true);  // 標記已選擇
                    });
                dropdownMenu.append(item);
            });
        },
        error: function (xhr, status, error) {
            console.error("獲取供應商列表失敗：" + error);
        }
    });

    // 監聽表單提交事件
    $("#submitMaterialForm").on("submit", function (event) {
        event.preventDefault();  // 阻止表單的默認提交行為

        console.log("Form submitted!");
        
        // 收集表單數據
        const materialName = $("#materialName").val();
        const supplierName = $("#dropdownMenuButton").text();
        const shipDay = $("#shipDay").val();
        const packAmount = $("#packAmount").val();
        const packPrice = $("#packPrice").val();
        const validDay = $("#validDay").val();

        console.log("Ship Day Value:", shipDay);  // 檢查 shipDay 是否正確

        // 檢查必要字段是否填寫
        if (!shipDay || shipDay === "") {
            alert("請填寫運送天數！");
            return;
        }

        // 檢查下拉選單是否已選擇供應商
        if (!$("#dropdownMenuButton").data("selected")) {
            alert("請選擇供應商！");
            return;
        }

        // 構建要傳送到後端的資料物件
        const formData = {
            materialName: materialName,
            supplier: supplierName,
            shipDay: shipDay,
            packAmount: packAmount,
            packPrice: packPrice,
            validDay: validDay
        };

        console.log("Form data being sent:", formData);  // 檢查發送的資料

        // 使用 jQuery 的 $.ajax 發送資料
        $.ajax({
            url: '/submitMaterial',  // 提交到後端的接口
            type: 'POST',
            contentType: 'application/json',  // 設置請求內容類型為 JSON
            data: JSON.stringify(formData),  // 將表單資料轉換為 JSON 字串
            success: function (response) {
                if (response.success) {
                    alert("新增成功！");
                    $("#submitMaterialForm")[0].reset();  // 清空表單
                    $("#dropdownMenuButton").text("請選擇供應商");  // 重置下拉選單
                    $("#dropdownMenuButton").data("selected", false);  // 重置選擇狀態
                } else {
                    alert("新增失敗：" + response.message);
                    $("#submitMaterialForm")[0].reset();  // 清空表單
                    $("#dropdownMenuButton").text("請選擇供應商");  // 重置下拉選單
                    $("#dropdownMenuButton").data("selected", false);  // 重置選擇狀態
                }
            },
            error: function (xhr, status, error) {
                alert("發生錯誤：" + error);
                $("#submitMaterialForm")[0].reset();  // 清空表單
                $("#dropdownMenuButton").text("請選擇供應商");  // 重置下拉選單
                $("#dropdownMenuButton").data("selected", false);  // 重置選擇狀態
            }
        });
    });
});
