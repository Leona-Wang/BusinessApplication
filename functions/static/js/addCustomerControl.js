$(document).ready(function () {
    console.log("Document is ready!");
    // 監聽表單提交事件
    $("#submitCustomerForm").on("submit", function (event) {
        event.preventDefault();  // 阻止表單的默認提交行為

        const customerName =$("#customerName").val();
        const customerPhone = $("#customerPhone").val();

        if (customerName.trim() === '') {
            alert('客戶名稱不能為空！');
            return; // 停止提交表單
        }
    
        if (customerPhone.trim() === '') {
            alert('電話號碼不能為空！');
            return; // 停止提交表單
        }
    
        // 檢查 supplierPhone 是否為全數字
        const phonePattern = /^[0-9]+$/; // 正則表達式，檢查是否全為數字
        if (!phonePattern.test(customerPhone)) {
            alert('電話號碼必須是全數字！');
            return; // 停止提交表單
        }

        // 構建要傳送到後端的資料物件
        const formData = {
            customerName: customerName,
            customerPhone:customerPhone
        };
        // 使用 jQuery 的 $.ajax 發送資料
        $.ajax({
            url: '/submitCustomer',  // 提交到後端的接口
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

document.getElementById('customerPhone').addEventListener('input', function () {
    const phoneInput = this.value;
    const phoneError = document.getElementById('phoneError');

    // 檢查是否為數字
    if (/^\d*$/.test(phoneInput)) {
        phoneError.style.display = 'none'; // 隱藏錯誤訊息
    } else {
        phoneError.style.display = 'block'; // 顯示錯誤訊息
    }
});