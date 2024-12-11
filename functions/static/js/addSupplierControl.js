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

    // 發送 AJAX 請求
    fetch(submitSupplierURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: new URLSearchParams({
            supplierName: supplierName,
            supplierPhone: supplierPhone,
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                document.getElementById('supplierName').value = '';
                document.getElementById('supplierPhone').value = '';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('提交失敗！');
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