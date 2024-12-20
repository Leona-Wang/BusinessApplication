const today = new Date();
const yyyy = today.getFullYear();
const mm = String(today.getMonth() + 1).padStart(2, '0'); // 月份補0
const dd = String(today.getDate()).padStart(2, '0'); // 日期補0

const minDate = `${yyyy}-${mm}-${dd}`; // 格式化為 YYYY-MM-DD

 // 設置 input 的最小日期
const dateInput = document.getElementById('importDate');
dateInput.min = minDate;
dateInput.value = minDate; // 可選：默認值設為當天
$(document).ready(function () {
    console.log("Document is ready!");

    // 獲取供應商列表
    $.ajax({
        url: '/getMaterialList',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var dropdownMenu = $("#materialDropdown");
            // 處理返回的 JSON 資料
            data.forEach(function (material) {
                var item = $('<a class="dropdown-item"></a>')
                    .text(material.materialName)  // 顯示供應商名稱
                    .attr("id", material.id)  // 儲存供應商 ID
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
    $("#submitInventoryForm").on("submit", function (event) {
        event.preventDefault();  // 阻止表單的默認提交行為

        console.log("Form submitted!");
        
        // 收集表單數據
        const materialName = $("#dropdownMenuButton").text();
        const importDate = document.querySelector('#importDay input[name="importDate"]').value;
        const amount = $("#amount").val();

        // 檢查必要字段是否填寫
        if (!amount || amount === "") {
            alert("請填寫進貨數量！");
            return;
        }

        // 檢查下拉選單是否已選擇供應商
        if (!$("#dropdownMenuButton").data("selected")) {
            alert("請選擇進貨原物料！");
            return;
        }

        // 構建要傳送到後端的資料物件
        const formData = {
            materialName: materialName,
            importDate:importDate,
            amount:amount
        };

        console.log("Form data being sent:", formData);  // 檢查發送的資料

        // 使用 jQuery 的 $.ajax 發送資料
        $.ajax({
            url: '/submitInventory',  // 提交到後端的接口
            type: 'POST',
            contentType: 'application/json',  // 設置請求內容類型為 JSON
            data: JSON.stringify(formData),  // 將表單資料轉換為 JSON 字串
            success: function (response) {
                if (response.success) {
                    alert("新增成功！");
                    location.reload();
                } else {
                    alert("新增失敗：" + response.message);
                }
            },
            error: function (xhr, status, error) {
                alert("發生錯誤：" + error);
            }
        });
    });
});
