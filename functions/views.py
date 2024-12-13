import json
from django.shortcuts import render
from django.http import JsonResponse
from functions.models.supplier import Supplier
from functions.models.material import Material
from functions.models.materialSource import MaterialSource
from functions.models.product import Product
from functions.models.ingredient import Ingredient


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
            materialList = []
            sources = MaterialSource.objects.filter(supplier_id=supplierID)
            if sources.exists():
                for source in sources:
                    material = Material.objects.get(id=source.material_id)
                    materialList.append(material)
            supplier.delete()
            if len(materialList) > 0:
                for material in materialList:
                    material.delete()

            return JsonResponse({"success": True, "message": "資料刪除成功"})
        except Supplier.DoesNotExist:
            return JsonResponse({"success": False, "message": "供應商不存在"})


def submitMaterial(request):
    if request.method == 'POST':
        try:
            # 打印原始請求資料以便調試
            print(request.body) # 打印原始的請求體，確保它是有效的 JSON

            # 解析 JSON 請求體
            data = json.loads(request.body)

            # 從解析的資料中獲取數據
            materialName = data.get('materialName')
            supplierName = data.get('supplier')
            shipDay = data.get('shipDay')
            packAmount = data.get('packAmount')
            packPrice = data.get('packPrice')
            validDay = data.get('validDay')

            print(
                f"""{materialName}
                  {supplierName}
                  {shipDay}
                  {packAmount}
                  {packPrice}
                  {validDay}"""
            )

            # 檢查是否有重複的原物料名稱
            checkMaterial = Material.objects.filter(materialName=materialName)

            # 確保供應商存在
            try:
                supplier = Supplier.objects.get(supplierName=supplierName)
            except Supplier.DoesNotExist:
                return JsonResponse({"success": False, "message": "供應商不存在"})

            supplierID = supplier.id

            # 如果原物料名稱未重複，則新增資料
            if not checkMaterial.exists():
                material = Material.objects.create(
                    materialName=materialName,
                    packAmount=packAmount,
                    packPrice=packPrice,
                    validDay=validDay,
                    shipDay=shipDay
                )
                # 創建物料來源
                MaterialSource.objects.create(material_id=material.id, supplier_id=supplierID)
                return JsonResponse({"success": True, "message": "新增成功"})

            # 如果原物料已存在
            else:
                return JsonResponse({"success": False, "message": "重複資料"})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "無效的 JSON 格式"})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "不支持的請求方法"})


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
                'shipDay': material.shipDay,
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
        shipDay = request.POST.get("shipDay").strip()
        supplierName = request.POST.get("supplierName").strip()

        try:
            material = Material.objects.get(id=materialID)
            material.materialName = materialName
            material.packPrice = packPrice
            material.packAmount = packAmount
            material.validDay = validDay
            material.shipDay = shipDay
            material.save()
            supplier = Supplier.objects.get(supplierName=supplierName)
            source = MaterialSource.objects.get(material_id=materialID)
            source.supplier_id = supplier.id
            source.save()
            ingredients = Ingredient.objects.filter(material_id=materialID)
            for ingredient in ingredients:
                ingredient.save()

            return JsonResponse({"success": True, "message": "更新成功"})
        except Supplier.DoesNotExist:
            return JsonResponse({"success": False, "message": "供應商不存在"})
        except ValueError:
            return JsonResponse({"success": False, "message": "validDay 格式錯誤"})


def deleteMaterial(request):
    if request.method == 'POST':
        materialID = request.POST.get("id")
        try:
            productList = []
            ingredients = Ingredient.objects.filter(material_id=materialID)
            if ingredients.exists():
                for ingredient in ingredients:
                    product = Product.objects.get(id=ingredient.product_id)
                    productList.append(product)

            material = Material.objects.filter(id=materialID)
            material.delete()
            if len(productList) > 0:
                for product in productList:
                    product.delete()
            return JsonResponse({"success": True, "message": "資料刪除成功"})
        except Supplier.DoesNotExist:
            return JsonResponse({"success": False, "message": "原物料不存在"})


def submitBOM(request):
    if request.method == 'POST':
        # 從表單中獲取數據
        data = json.loads(request.body)

        productName = data.get('productName')
        productPrice = data.get('productPrice')

        checkProduct = Product.objects.filter(productName=productName)
        print(len(checkProduct) == 0)

        if len(checkProduct) == 0:
            Product.objects.create(productName=productName, productPrice=productPrice)
            materials = data.get('materials', [])
            for material in materials:
                materialName = material.get('materialName')
                unit = material.get('unit')
                try:
                    materialID = Material.objects.get(materialName=materialName).id
                    productID = Product.objects.get(productName=productName).id
                    Ingredient.objects.create(material_id=materialID, product_id=productID, unit=unit)
                    return JsonResponse({"success": True, "message": "更新成功"})
                except Material.DoesNotExist:
                    return JsonResponse({"success": False, "message": f"材料 {materialName} 不存在"})
                except Product.DoesNotExist:
                    return JsonResponse({"success": False, "message": f"產品 {productName} 不存在"})
        else:
            return JsonResponse({"success": False, "message": "重複產品資料"})


def getBOMList(request):
    try:
        products = Product.objects.all()

        BOMList = []
        for product in products:
            productID = product.id
            ingredients = Ingredient.objects.filter(product_id=productID)
            materialNameList = []
            unitList = []
            for ingredient in ingredients:
                materialID = ingredient.material_id
                material = Material.objects.get(id=materialID)
                materialNameList.append(material.materialName)
                unitList.append(ingredient.unit)

            BOMData = {
                'id': product.id,
                'productName': product.productName,
                'productPrice': product.productPrice,
                'materialNames': materialNameList,
                'units': unitList
            }
            BOMList.append(BOMData)

        return JsonResponse(BOMList, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
