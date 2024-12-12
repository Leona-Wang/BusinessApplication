const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
document.getElementById('submitSupplierForm').addEventListener('submit', function (e) {
    e.preventDefault(); // 阻止表單默認提交行為

    // 獲取表單資料
    const supplierName = document.getElementById('supplierName').value;
    const supplierPhone = document.getElementById('supplierPhone').value;

    // 檢查兩個欄位是否為空
    if (supplierName.trim() === '') {
        alert('供應商名稱不能為空！');
        return; // 停止提交表單
    }

    if (supplierPhone.trim() === '') {
        alert('電話號碼不能為空！');
        return; // 停止提交表單
    }

    // 檢查 supplierPhone 是否為全數字
    const phonePattern = /^[0-9]+$/; // 正則表達式，檢查是否全為數字
    if (!phonePattern.test(supplierPhone)) {
        alert('電話號碼必須是全數字！');
        return; // 停止提交表單
    }

    $.ajax({
        url: '/submitSupplier', // Django 後端 API 路徑
        type: 'POST',          // 使用 POST 請求
        data: {
            supplierName: supplierName,
            supplierPhone: supplierPhone,      // 傳送的資料 ID
        },
        success: function (response) {
            if (response.success) {
                alert("新增成功！");
                document.getElementById('supplierName').value = '';
                document.getElementById('supplierPhone').value = '';
            } else {
                alert("新增失敗：" + response.message);
                document.getElementById('supplierName').value = '';
                document.getElementById('supplierPhone').value = '';
            }
        },
        error: function (xhr, status, error) {
            alert("發生錯誤：" + error);
        }
    });
});
document.getElementById('supplierPhone').addEventListener('input', function () {
    const phoneInput = this.value;
    const phoneError = document.getElementById('phoneError');

    // 檢查是否為數字
    if (/^\d*$/.test(phoneInput)) {
        phoneError.style.display = 'none'; // 隱藏錯誤訊息
    } else {
        phoneError.style.display = 'block'; // 顯示錯誤訊息
    }
});