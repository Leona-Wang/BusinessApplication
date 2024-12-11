from django.shortcuts import render
from django.http import JsonResponse
from functions.models.supplier import Supplier


def index(request):
    return render(request, 'index.html')


def showBOM(request):
    return render(request, 'showBOM.html')


def addBOM(request):
    return render(request, 'addBOM.html')


def showMaterial(request):
    return render(request, 'showMaterial.html')


def addMaterial(request):
    return render(request, 'addMaterial.html')


def addInventory(request):
    return render(request, 'addInventory.html')


def showInventory(request):
    return render(request, 'showInventory.html')


def addSupplier(request):
    return render(request, 'addSupplier.html')


def showSupplier(request):
    return render(request, 'showSupplier.html')


def addCustomer(request):
    return render(request, 'addCustomer.html')


def showCustomer(request):
    return render(request, 'showCustomer.html')


def addOrder(request):
    return render(request, 'addOrder.html')


def showOrder(request):
    return render(request, 'showOrder.html')


def addWalkIn(request):
    return render(request, 'addWalkIn.html')


def showWalkIn(request):
    return render(request, 'showWalkIn.html')


def analysis(request):
    return render(request, 'analysis.html')


def submitSupplier(request):
    if request.method == 'POST':
        # 從表單中獲取數據
        supplierName = request.POST.get('supplierName')
        supplierPhone = request.POST.get('supplierPhone')

        # 打印或處理數據
        print(f"供應商名稱: {supplierName}, 供應商電話: {supplierPhone}")

        # 保存到數據庫的示例（可選）
        Supplier.objects.create(supplierName=supplierName, supplierPhone=supplierPhone)

        # 返回 JSON 成功響應
        return JsonResponse({
            'message': '資料已成功提交',
            'supplier_name': supplierName,
            'supplier_phone': supplierPhone,
        })

    # GET 請求時返回模板
    #return render(request, 'addSupplier.html')
