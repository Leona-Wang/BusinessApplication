// 獲取訂單類型的 radio buttons
const orderTypeInputs = document.querySelectorAll('input[name="orderType"]');
const oneTimeDayDiv = document.getElementById('oneTimeDay');
const recurringDayDiv = document.getElementById('recurringDay');
// 監聽訂單類型變化
orderTypeInputs.forEach(input => {
    input.addEventListener('change', () => {
        if (input.value === 'oneTime') {
            // 單次訂單時顯示 oneTimeDay，隱藏 recurringDay
            oneTimeDayDiv.style.display = 'block';
            recurringDayDiv.style.display = 'none';
        } else if (input.value === 'recurring') {
            // 固定訂單時顯示 recurringDay，隱藏 oneTimeDay
            oneTimeDayDiv.style.display = 'none';
            recurringDayDiv.style.display = 'block';
        }
    });
});

 // 獲取當前日期
/*const today = new Date();
const yyyy = today.getFullYear();
const mm = String(today.getMonth() + 1).padStart(2, '0'); // 月份補0
const dd = String(today.getDate()).padStart(2, '0'); // 日期補0

const minDate = `${yyyy}-${mm}-${dd}`; // 格式化為 YYYY-MM-DD

 // 設置 input 的最小日期
const dateInput = document.getElementById('dueDate');
dateInput.min = minDate;
dateInput.value = minDate; // 可選：默認值設為當天
*/
$(document).ready(function () {
    console.log("Document is ready!");

    $('#productContainer').on('click', '.productDropdown', function () {
        const dropdownMenu = $(this).siblings('.dropdown-menu');
        if (dropdownMenu.children().length === 0) { // 避免重複載入
            loadProductDropdown(dropdownMenu);
        }
    });

    if ($('#productContainer').children().length === 0) {
        const initialProductRow = generateProductRow();
        $('#productContainer').append(initialProductRow);
        loadProductDropdown(initialProductRow.find('.dropdown-menu'));
    }

    $('#productContainer').on('click', '.addRowButton', function () {
        const newProductRow = generateProductRow();
        $(this).closest('.input-row').after(newProductRow);
        loadProductDropdown(newProductRow.find('.dropdown-menu'));
    });

    // 刪除按鈕功能
    $('#productContainer').on('click', '.deleteButton', function () {
        const confirmed = confirm('確定要刪除此項材料嗎？');
        if (confirmed) {
            $(this).closest('.input-row').remove();

            if ($('#productContainer').children().length === 0) {
                const initialProductRow = generateProductRow();
                $('#productContainer').append(initialProductRow);
                loadProductDropdown(initialProductRow.find('.dropdown-menu'));
            }
        }
    });

    function loadProductDropdown(dropdownMenu) {
        $.ajax({
            url: '/getBOMList',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                dropdownMenu.empty(); // 清空現有的下拉選單
                data.forEach(function (product) {
                    const item = $('<a class="dropdown-item"></a>')
                        .text(product.productName)
                        .attr('id', product.id)
                        .on('click', function () {
                            // 更新按鈕文字
                            const selectedText = $(this).text();
                            dropdownMenu.siblings('.dropdown-toggle').text(selectedText);
                        });
                    dropdownMenu.append(item);
                });
            },
            error: function () {
                console.error('無法載入材料清單');
            }
        });
    }

    // 生成材料行的 HTML 結構
    function generateProductRow() {
        return $(`
            <div class="row input-row">
                <div class="col-lg-4 mb-4">
                    <div class="card shadow mb-4">
                        <div class="card-header py-3">
                            <h6 class="m-0 font-weight-bold text-primary">訂購餐點</h6>
                        </div>
                        <div class="card-body">
                            <div class="dropdown productName no-arrow mb-4">
                                <button class="productDropdown col-lg-12 btn btn-secondary dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    請選擇餐點
                                </button>
                                <div class="col-lg-12 dropdown-menu" aria-labelledby="dropdownMenuButton" style="">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 mb-4">
                    <div class="card shadow mb-4">
                        <div class="card-header py-3">
                            <h6 class="m-0 font-weight-bold text-primary">訂購數量(單位:份)</h6>
                        </div>
                        <div class="card-body">
                            <div class="input-group">
                                <input type="number" id="amount" class="amount form-control bg-light border-1 small" placeholder="1" min="1" required>
                            </div>
                            <div><br></div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 mb-4">
                    <div class="card shadow mb-4">
                        <div class="card-body">
                            <a class="col-lg-12 d-flex justify-content-start addRowButton btn btn-info btn-icon-split">
                                <span class="icon text-white-50">
                                    <i class="fas fa-info-circle"></i>
                                </span>
                                <span class="text">新增下一種餐點</span>
                            </a>
                        </div>
                        <div class="card-body">
                            <a class="col-lg-12 d-flex justify-content-start deleteButton btn btn-danger btn-icon-split">
                                <span class="icon text-white-50">
                                    <i class="fas fa-trash"></i>
                                </span>
                                <span class="text">刪除這項餐點</span>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        `);
    }

    // 獲取供應商列表
    $.ajax({
        url: '/getCustomerList',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var dropdownMenu = $("#customerDropdown");
            // 處理返回的 JSON 資料
            data.forEach(function (customer) {
                var item = $('<a class="dropdown-item"></a>')
                    .text(customer.customerName)  // 顯示供應商名稱
                    .attr("id", customer.id)  // 儲存供應商 ID
                    .on("click", function () {
                        // 當選項被點擊時觸發
                        var selectedCustomer = $(this).text();  // 獲取選中供應商的名稱
                        $("#customerDropdownButton").text(selectedCustomer);  // 更新按鈕文字
                        $("#customerDropdownButton").data("selected", true);  // 標記已選擇
                    });
                dropdownMenu.append(item);
            });
        },
        error: function (xhr, status, error) {
            console.error("獲取供應商列表失敗：" + error);
        }
    });

    $('#submitOrderForm').on('submit', function (e) {
        e.preventDefault(); // 防止默認表單提交，改用 AJAX 提交
        let customerName=$('#customerDropdownButton').text().trim();
        let type = document.querySelector('input[name="orderType"]:checked').value;
        let isValid = true; // 初始化表單有效性標誌
        if (customerName==="請選擇客戶"){
            alert("請選擇客戶！");
            isValid = false;
            return false;
        }
        // 動態取得對應輸入框的值
        let inputDay = null;

        if (type === 'oneTime') {
            // 單次訂單 => 取交貨日 (oneTimeDay)
            const oneTimeInput = document.querySelector('#oneTimeDay input[name="dueDate"]');
            if (oneTimeInput.value.trim() !== '') {
                inputDay = oneTimeInput.value.trim();
            }else{
                alert("請輸入交貨日期!");
                isValid = false;
                return false;
            }
        } else if (type === 'recurring') {
            // 固定訂單 => 取所有被選中的 checkbox
            const recurringInputs = document.querySelectorAll('#recurringDay input[type="checkbox"]:checked');
            inputDay = Array.from(recurringInputs).map(checkbox => checkbox.value).join(',');
            if (!inputDay){
                alert("請選擇至少一個交貨日!");
                isValid = false;
                return false;
            }
        }
        
        
        // 收集表單中的資料
        let formData = {
            customerName: customerName,
            type: type,
            inputDay:inputDay,
            products: []
        };
        
        let productNames = [];
        
    
        $('#productContainer .input-row').each(function () {
            let productName = $(this).find('.productDropdown').text().trim();
            let amount = $(this).find('.amount').val();
    
            // 驗證是否選擇了材料
            if (productName === "請選擇餐點") {
                alert("請選擇餐點！");
                isValid = false;
                return false; // 終止當前迴圈
            }
    
            // 驗證是否有重複的材料
            if (productNames.includes(productName)) {
                alert("重複的餐點！請計算總和再填入");
                isValid = false;
                return false; // 終止當前迴圈
            }
    
            // 驗證該行是否選擇了材料且數量有效
            if (productName && amount && amount > 0) {
                productNames.push(productName);
                formData.products.push({
                    productName: productName,
                    amount: amount
                });
                
            } else {
                alert("請選擇餐點並輸入有效的數量！");
                isValid = false;
                return false; // 終止當前迴圈
            }
        });

        
        
        // 如果表單無效，停止提交
        if (!isValid) {
            return;
        }
        // 使用 AJAX 發送資料到後端
        $.ajax({
            url: '/submitOrder', // 後端處理請求的 URL
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(formData), // 將資料轉換為 JSON 字串
            success: function (response) {
                if (response.success) {
                    alert("新增成功！");
                    location.reload();
                } else {
                    alert("新增失敗：" + response.message);
                }
            },
            error: function (xhr, status, error) {
                // 處理錯誤回應
                console.error('提交資料時發生錯誤:', error);
                alert('提交資料時發生錯誤。');
            }
        });
    });
});