from django.shortcuts import render
from django.http import JsonResponse
from functions.models.supplier import Supplier
from functions.models.material import Material
from functions.models.materialSource import MaterialSource


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

        checkSupplierName = Supplier.objects.filter(supplierName=supplierName)
        checkSupplierPhone = Supplier.objects.filter(supplierName=supplierName)

        if checkSupplierName.exists() == False and checkSupplierPhone.exists() == False:
            Supplier.objects.create(supplierName=supplierName, supplierPhone=supplierPhone)
            return JsonResponse({"success": True, "message": "更新成功"})
        else:
            return JsonResponse({"success": False, "message": "重複資料"})
        # 保存到數據庫的示例（可選）

    # GET 請求時返回模板
    #return render(request, 'addSupplier.html')


def getSupplierList(request):
    try:
        supplierList = Supplier.objects.all()
        supplierData = list(supplierList.values('id', 'supplierName', 'supplierPhone'))
        return JsonResponse(supplierData, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def updateSupplier(request):
    if request.method == 'POST':
        supplierID = request.POST.get("id")
        supplierName = request.POST.get("supplierName")
        supplierPhone = request.POST.get("supplierPhone")
        try:
            supplier = Supplier.objects.get(id=supplierID)
            supplier.supplierName = supplierName
            supplier.supplierPhone = supplierPhone
            supplier.save()
            return JsonResponse({"success": True, "message": "更新成功"})
        except Supplier.DoesNotExist:
            return JsonResponse({"success": False, "message": "供應商不存在"})


def deleteSupplier(request):
    if request.method == 'POST':
        supplierID = request.POST.get("id")
        try:
            supplier = Supplier.objects.filter(id=supplierID)
            supplier.delete()
            return JsonResponse({"success": True, "message": "資料刪除成功"})
        except Supplier.DoesNotExist:
            return JsonResponse({"success": False, "message": "供應商不存在"})


def submitMaterial(request):
    if request.method == 'POST':
        # 從表單中獲取數據
        materialName = request.POST.get('materialName')
        supplierName = request.POST.get('supplierName')
        packAmount = request.POST.get('packAmount')
        packPrice = request.POST.get('packPrice')
        validDay = request.POST.get('validDay')

        checkMaterial = Material.objects.filter(materialName=materialName)
        supplier = Supplier.objects.get(supplierName=supplierName)
        supplierID = supplier.id

        if checkMaterial.exists() == False:
            Material.objects.create(
                materialName=materialName, packAmount=packAmount, packPrice=packPrice, validDay=validDay
            ).save()
            material = Material.objects.get(materialName=materialName)
            materialID = material.id
            MaterialSource.objects.create(material_id=materialID, supplier_id=supplierID)
            return JsonResponse({"success": True, "message": "更新成功"})
        else:
            return JsonResponse({"success": False, "message": "重複資料"})


def getMaterialList(request):
    try:
        materials = Material.objects.all()

        materialList = []
        for material in materials:
            source = MaterialSource.objects.get(material_id=material.id)
            supplier = Supplier.objects.get(id=source.supplier_id)
            materialData = {
                'id': material.id,
                'materialName': material.materialName,
                'packAmount': material.packAmount,
                'packPrice': material.packPrice,
                'validDay': material.validDay,
                'supplierName':
                    supplier.supplierName # 添加供應商名稱
            }
            materialList.append(materialData)

        return JsonResponse(materialList, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def updateMaterial(request):
    if request.method == 'POST':
        materialID = request.POST.get("id").strip()
        materialName = request.POST.get("materialName").strip()
        packPrice = request.POST.get("packPrice").strip()
        packAmount = request.POST.get("packAmount").strip()
        validDay = request.POST.get("validDay").strip()
        supplierName = request.POST.get("supplierName").strip()

        try:
            material = Material.objects.get(id=materialID)
            material.materialName = materialName
            material.packPrice = packPrice
            material.packAmount = packAmount
            material.validDay = validDay
            material.save()
            supplier = Supplier.objects.get(supplierName=supplierName)
            source = MaterialSource.objects.get(material_id=materialID)
            source.supplier_id = supplier.id
            source.save()

            return JsonResponse({"success": True, "message": "更新成功"})
        except Supplier.DoesNotExist:
            return JsonResponse({"success": False, "message": "供應商不存在"})
        except ValueError:
            return JsonResponse({"success": False, "message": "validDay 格式錯誤"})


def deleteMaterial(request):
    if request.method == 'POST':
        materialID = request.POST.get("id")
        try:
            material = Material.objects.filter(id=materialID)
            source = MaterialSource.objects.filter(material_id=materialID)
            source.delete()
            material.delete()
            return JsonResponse({"success": True, "message": "資料刪除成功"})
        except Supplier.DoesNotExist:
            return JsonResponse({"success": False, "message": "原物料不存在"})
