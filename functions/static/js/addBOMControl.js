$(document).ready(function () {
    // 檢查 #materialContainer 是否為空，若空則自動生成一段初始內容
    $('#materialContainer').on('click', '.materialDropdown', function () {
        const dropdownMenu = $(this).siblings('.dropdown-menu');
        if (dropdownMenu.children().length === 0) { // 避免重複載入
            loadMaterialDropdown(dropdownMenu);
        }
    });

    if ($('#materialContainer').children().length === 0) {
        const initialMaterialRow = generateMaterialRow();
        $('#materialContainer').append(initialMaterialRow);
        loadMaterialDropdown(initialMaterialRow.find('.dropdown-menu'));
    }

    // 綁定事件委託到 #materialContainer，監聽所有「新增下一種材料」按鈕
    $('#materialContainer').on('click', '.addRowButton', function () {
        const newMaterialRow = generateMaterialRow();
        $(this).closest('.input-row').after(newMaterialRow);
        loadMaterialDropdown(newMaterialRow.find('.dropdown-menu'));
    });

    // 刪除按鈕功能
    $('#materialContainer').on('click', '.deleteButton', function () {
        const confirmed = confirm('確定要刪除此項材料嗎？');
        if (confirmed) {
            $(this).closest('.input-row').remove();

            // 如果刪除後 #materialContainer 為空，生成一段初始內容
            if ($('#materialContainer').children().length === 0) {
                const initialMaterialRow = generateMaterialRow();
                $('#materialContainer').append(initialMaterialRow);
                loadMaterialDropdown(initialMaterialRow.find('.dropdown-menu'));
            }
        }
    });

    $('#submitBOMForm').on('submit', function (e) {
        e.preventDefault(); // 防止默認表單提交，改用 AJAX 提交
        
        // 收集表單中的資料
        const formData = {
            productName: $('#productName').val(),
            productPrice: $('#productPrice').val(),
            materials: []
        };
        
        let materialNames = [];
        let isValid = true; // 初始化表單有效性標誌
    
        // 遍歷 #materialContainer 中的所有材料行
        $('#materialContainer .input-row').each(function () {
            const materialName = $(this).find('.materialDropdown').text().trim();
            const unit = $(this).find('.unit').val();
    
            // 驗證是否選擇了材料
            if (materialName === "請選擇材料") {
                alert("請選擇材料！");
                isValid = false;
                return false; // 終止當前迴圈
            }
    
            // 驗證是否有重複的材料
            if (materialNames.includes(materialName)) {
                alert("重複的材料！請計算總和再填入");
                isValid = false;
                return false; // 終止當前迴圈
            }
    
            // 驗證該行是否選擇了材料且數量有效
            if (materialName && unit && unit > 0) {
                materialNames.push(materialName);
                formData.materials.push({
                    materialName: materialName,
                    unit: unit
                });
            } else {
                alert("請選擇材料並輸入有效的數量！");
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
            url: '/submitBOM', // 後端處理請求的 URL
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(formData), // 將資料轉換為 JSON 字串
            success: function (response) {
                if (response.success) {
                    alert("新增成功！");
                    $('#submitBOMForm')[0].reset();  // 重設表單內容
                    // 如果有動態添加的行（例如材料行），也需要清空這些動態元素
                    $('#materialContainer').empty(); // 清空材料容器
                    const initialMaterialRow = generateMaterialRow();
                    $('#materialContainer').append(initialMaterialRow);
                    loadMaterialDropdown(initialMaterialRow.find('.dropdown-menu'));
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
    
    // 從伺服器載入材料清單並填充到指定的下拉選單中
    function loadMaterialDropdown(dropdownMenu) {
        $.ajax({
            url: '/getMaterialList',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                dropdownMenu.empty(); // 清空現有的下拉選單
                data.forEach(function (material) {
                    const item = $('<a class="dropdown-item"></a>')
                        .text(material.materialName)
                        .attr('id', material.id)
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
    function generateMaterialRow() {
        return $(`
            <div class="row input-row">
                <div class="col-lg-4 mb-4">
                    <div class="card shadow mb-4">
                        <div class="card-header py-3">
                            <h6 class="m-0 font-weight-bold text-primary">使用材料</h6>
                        </div>
                        <div class="card-body">
                            <div class="dropdown materialName no-arrow mb-4">
                                <button class="materialDropdown col-lg-12 btn btn-secondary dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    請選擇材料
                                </button>
                                <div class="col-lg-12 dropdown-menu" aria-labelledby="dropdownMenuButton"></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 mb-4">
                    <div class="card shadow mb-4">
                        <div class="card-header py-3">
                            <h6 class="m-0 font-weight-bold text-primary">使用數量(單位:個)</h6>
                        </div>
                        <div class="card-body">
                            <div class="input-group">
                                <input type="number" id="unit" class="unit form-control bg-light border-1 small" placeholder="1" min="1" required>
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
                                <span class="text">新增下一種材料</span>
                            </a>
                        </div>
                        <div class="card-body">
                            <a class="col-lg-12 d-flex justify-content-start deleteButton btn btn-danger btn-icon-split">
                                <span class="icon text-white-50">
                                    <i class="fas fa-trash"></i>
                                </span>
                                <span class="text">刪除這項材料</span>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        `);
    }
});
