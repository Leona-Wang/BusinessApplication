import json
import statistics
import math
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from django.db.models import F, Sum, Max, Min, Count, Case, When, Value, Q
from datetime import date, timedelta
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.db import transaction, models
from functions.models.supplier import Supplier
from functions.models.material import Material
from functions.models.materialSource import MaterialSource
from functions.models.product import Product
from functions.models.ingredient import Ingredient
from functions.models.inventory import Inventory
from functions.models.customer import Customer
from functions.models.order import Order
from functions.models.orderDetail import OrderDetail
from functions.models.refreshRecord import RefreshRecord
from django.db.models import Subquery, OuterRef, Case, When, Value, F
from django.db.models import Count, Sum, Min
from datetime import datetime, timedelta


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
    refreshQuantity()
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
    getRFM()
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
            removeSupplier(supplierID=supplierID)
            return JsonResponse({"success": True, "message": "資料刪除成功"})
        except Supplier.DoesNotExist:
            return JsonResponse({"success": False, "message": "供應商不存在"})


def submitMaterial(request):
    if request.method == 'POST':
        try:

            # 解析 JSON 請求體
            data = json.loads(request.body)

            # 從解析的資料中獲取數據
            materialName = data.get('materialName')
            supplierName = data.get('supplier')
            shipDay = data.get('shipDay')
            packAmount = data.get('packAmount')
            packPrice = data.get('packPrice')
            validDay = data.get('validDay')

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
            removeMaterial(materialID=materialID)
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

        if len(checkProduct) == 0:
            Product.objects.create(productName=productName, productPrice=productPrice)
            materials = data.get('materials', [])
            print(f"lenth:{len(materials)}")
            for material in materials:
                materialName = material.get('materialName')
                unit = material.get('unit')
                try:
                    materialID = Material.objects.get(materialName=materialName).id
                    productID = Product.objects.get(productName=productName).id
                    Ingredient.objects.create(material_id=materialID, product_id=productID, unit=unit)
                except Material.DoesNotExist:
                    return JsonResponse({"success": False, "message": f"材料 {materialName} 不存在"})
                except Product.DoesNotExist:
                    return JsonResponse({"success": False, "message": f"產品 {productName} 不存在"})
            return JsonResponse({"success": True, "message": "更新成功"})
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


def deleteProduct(request):
    if request.method == 'POST':
        productID = request.POST.get("id")
        try:
            removeProduct(productID=productID)
            return JsonResponse({"success": True, "message": "資料刪除成功"})
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "message": "產品不存在"})


def editProduct(request, productID):
    print(f"Editing product with ID: {productID}")
    product = get_object_or_404(Product, id=productID)

    # 查找與這個 product 相關聯的所有 material
    ingredients = Ingredient.objects.filter(product=product)
    materials = Material.objects.all() # 獲取所有可用的材料選項

    return render(request, 'updateBOM.html', {'product': product, 'ingredients': ingredients, 'materials': materials})


def updateBOM(request):
    print("in")
    if request.method == 'POST':
        # 從表單中獲取數據
        data = json.loads(request.body)

        productName = data.get('productName')
        productPrice = data.get('productPrice')

        product = Product.objects.get(productName=productName)
        product.productPrice = productPrice
        product.save()
        productID = product.id
        materials = data.get('materials', [])
        ingredients = Ingredient.objects.filter(product_id=productID)
        ingredients.delete()
        for material in materials:
            materialName = material.get('materialName')
            unit = material.get('unit')
            try:
                materialID = Material.objects.get(materialName=materialName).id
                Ingredient.objects.create(material_id=materialID, product_id=productID, unit=unit)
            except Material.DoesNotExist:
                return JsonResponse({"success": False, "message": f"材料 {materialName} 不存在"})
            except Product.DoesNotExist:
                return JsonResponse({"success": False, "message": f"產品 {productName} 不存在"})
        return JsonResponse({"success": True, "message": "更新成功"})


def submitCustomer(request):
    if request.method == 'POST':
        # 從表單中獲取數據
        data = json.loads(request.body)

        customerName = data.get('customerName')
        customerPhone = data.get('customerPhone')

        checkCustomerName = Customer.objects.filter(customerName=customerName)
        checkCustomerPhone = Customer.objects.filter(customerPhone=customerPhone)

        if checkCustomerName.exists() == False and checkCustomerPhone.exists() == False:
            Customer.objects.create(customerName=customerName, customerPhone=customerPhone)
            return JsonResponse({"success": True, "message": "更新成功"})
        else:
            return JsonResponse({"success": False, "message": "重複資料"})


def getCustomerList(request):
    try:
        customerList = Customer.objects.all()
        customerData = list(customerList.values('id', 'customerName', 'customerPhone'))
        return JsonResponse(customerData, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def updateCustomer(request):
    if request.method == 'POST':
        customerID = request.POST.get("id")
        customerName = request.POST.get("customerName")
        customerPhone = request.POST.get("customerPhone")
        try:
            customer = Customer.objects.get(id=customerID)
            customer.customerName = customerName
            customer.customerPhone = customerPhone
            customer.save()
            return JsonResponse({"success": True, "message": "更新成功"})
        except Supplier.DoesNotExist:
            return JsonResponse({"success": False, "message": "供應商不存在"})


def deleteCustomer(request):
    if request.method == 'POST':
        customerID = request.POST.get("id")
        try:
            removeCustomer(customerID=customerID)
            return JsonResponse({"success": True, "message": "資料刪除成功"})
        except Supplier.DoesNotExist:
            return JsonResponse({"success": False, "message": "客戶不存在"})


def submitOrder(request):
    if request.method == 'POST':
        # 從表單中獲取數據
        data = json.loads(request.body)

        customerName = data.get('customerName')
        orderType = data.get('type')
        inputDay = data.get('inputDay')
        customer = Customer.objects.get(customerName=customerName)
        order = Order.objects.create(customer=customer, type=orderType)
        if orderType == 'oneTime':
            orderDate = inputDay
            order.orderDate = inputDay
        else:
            dayList = inputDay.split(',')
            for day in dayList:
                match day:
                    case "Mon":
                        order.mon = 1
                    case "Tue":
                        order.tue = 1
                    case "Wed":
                        order.wed = 1
                    case "Thu":
                        order.thu = 1
                    case "Fri":
                        order.fri = 1
        order.save()
        products = data.get('products', [])
        for product in products:
            productName = product.get('productName')
            amount = product.get('amount')
            product = Product.objects.get(productName=productName)
            try:
                OrderDetail.objects.create(order=order, product=product, amount=amount)
            except Product.DoesNotExist:
                return JsonResponse({"success": False, "message": f"產品 {productName} 不存在"})
        return JsonResponse({"success": True, "message": "更新成功"})


def deleteOrder(request):
    if request.method == 'POST':
        orderID = request.POST.get("id")
        try:
            removeOrder(orderID=orderID)
            return JsonResponse({"success": True, "message": "資料刪除成功"})
        except Supplier.DoesNotExist:
            return JsonResponse({"success": False, "message": "訂單不存在"})


def getOneTimeOrderList(request):
    try:
        orders = Order.objects.filter(type="oneTime").order_by('-orderDate')
        oneTimeOrderList = []
        for order in orders:
            orderID = order.id
            customer = order.customer
            customerName = customer.customerName
            customerPhone = customer.customerPhone
            orderDate = order.orderDate
            orderDate = orderDate.strftime("%Y-%m-%d")
            orderDetails = OrderDetail.objects.filter(order=order)
            productNameList = []
            amountList = []
            for orderDetail in orderDetails:
                product = orderDetail.product
                productNameList.append(product.productName)
                amountList.append(orderDetail.amount)
            oneTimeOrderData = {
                'id': orderID,
                'customerName': customerName,
                'customerPhone': customerPhone,
                'orderDate': orderDate,
                'productNames': productNameList,
                'amounts': amountList
            }
            oneTimeOrderList.append(oneTimeOrderData)
        return JsonResponse(oneTimeOrderList, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def getRecurringOrderList(request):
    try:
        orders = Order.objects.filter(type="recurring")
        recurringOrderList = []
        for order in orders:
            orderID = order.id
            customer = order.customer
            customerName = customer.customerName
            customerPhone = customer.customerPhone
            orderDays = []
            if order.mon == 1:
                orderDays.append("一")
            if order.tue == 1:
                orderDays.append("二")
            if order.wed == 1:
                orderDays.append("三")
            if order.thu == 1:
                orderDays.append("四")
            if order.fri == 1:
                orderDays.append("五")
            orderDetails = OrderDetail.objects.filter(order=order)
            productNameList = []
            amountList = []
            for orderDetail in orderDetails:
                product = orderDetail.product
                productNameList.append(product.productName)
                amountList.append(orderDetail.amount)
            recurringOrderData = {
                'id': orderID,
                'customerName': customerName,
                'customerPhone': customerPhone,
                'orderDate': ''.join(orderDays),
                'productNames': productNameList,
                'amounts': amountList
            }
            recurringOrderList.append(recurringOrderData)
        return JsonResponse(recurringOrderList, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def getTodayOrderList(request):
    try:
        today = datetime.now().date()
        oneTimeOrders = Order.objects.filter(type="oneTime", orderDate__date=today)
        todayOrderList = []
        for oneTimeOrder in oneTimeOrders:
            orderID = oneTimeOrder.id
            customer = oneTimeOrder.customer
            customerName = customer.customerName
            customerPhone = customer.customerPhone
            orderDate = oneTimeOrder.orderDate
            orderDate = orderDate.strftime("%Y-%m-%d")
            orderDetails = OrderDetail.objects.filter(order=oneTimeOrder)
            productNameList = []
            amountList = []
            for orderDetail in orderDetails:
                product = orderDetail.product
                productNameList.append(product.productName)
                amountList.append(orderDetail.amount)
            oneTimeOrderData = {
                'id': orderID,
                'customerName': customerName,
                'customerPhone': customerPhone,
                'orderDate': orderDate,
                'productNames': productNameList,
                'amounts': amountList
            }
            todayOrderList.append(oneTimeOrderData)
        weekdayMap = {
            0: 'mon',
            1: 'tue',
            2: 'wed',
            3: 'thu',
            4: 'fri',
        }
        todayDay = datetime.now().weekday() # 獲取 0-6 的值
        todayColumn = weekdayMap.get(todayDay)
        if todayColumn:
            recurringOrders = Order.objects.filter(**{todayColumn: 1})
            for recurringOrder in recurringOrders:
                orderID = recurringOrder.id
                customer = recurringOrder.customer
                customerName = customer.customerName
                customerPhone = customer.customerPhone
                orderDays = []
                if recurringOrder.mon == 1:
                    orderDays.append("一")
                if recurringOrder.tue == 1:
                    orderDays.append("二")
                if recurringOrder.wed == 1:
                    orderDays.append("三")
                if recurringOrder.thu == 1:
                    orderDays.append("四")
                if recurringOrder.fri == 1:
                    orderDays.append("五")
                orderDetails = OrderDetail.objects.filter(order=recurringOrder)
                productNameList = []
                amountList = []
                for orderDetail in orderDetails:
                    product = orderDetail.product
                    productNameList.append(product.productName)
                    amountList.append(orderDetail.amount)
                recurringOrderData = {
                    'id': orderID,
                    'customerName': customerName,
                    'customerPhone': customerPhone,
                    'orderDate': ''.join(orderDays),
                    'productNames': productNameList,
                    'amounts': amountList
                }
                todayOrderList.append(recurringOrderData)
        return JsonResponse(todayOrderList, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def editOrder(request, orderID):
    print(f"Editing product with ID: {orderID}")
    order = get_object_or_404(Order, id=orderID)
    customers = Customer.objects.all()
    orderDetails = OrderDetail.objects.filter(order=order)
    products = Product.objects.all()
    return render(
        request, 'updateOrder.html', {
            'order': order,
            'customers': customers,
            'orderDetails': orderDetails,
            'products': products
        }
    )


def updateOrder(request):
    if request.method == 'POST':
        # 從表單中獲取數據
        data = json.loads(request.body)

        orderID = data.get('orderID')
        order = Order.objects.get(id=orderID)
        customerName = data.get('customerName')
        orderType = data.get('type')
        inputDay = data.get('inputDay')
        order.type = orderType
        if orderType == 'oneTime':
            order.orderDate = inputDay
        else:
            dayList = inputDay.split(',')
            order.mon = 0
            order.tue = 0
            order.wed = 0
            order.thu = 0
            order.fri = 0
            for day in dayList:
                match day:
                    case "Mon":
                        order.mon = 1
                    case "Tue":
                        order.tue = 1
                    case "Wed":
                        order.wed = 1
                    case "Thu":
                        order.thu = 1
                    case "Fri":
                        order.fri = 1
        order.save()
        orderDetail = OrderDetail.objects.filter(order=order)
        orderDetail.delete()
        products = data.get('products', [])
        for product in products:
            productName = product.get('productName')
            amount = product.get('amount')
            product = Product.objects.get(productName=productName)
            try:
                OrderDetail.objects.create(order=order, product=product, amount=amount)
            except Product.DoesNotExist:
                return JsonResponse({"success": False, "message": f"產品 {productName} 不存在"})
        return JsonResponse({"success": True, "message": "更新成功"})


def submitInventory(request):
    if request.method == 'POST':
        # 從表單中獲取數據
        data = json.loads(request.body)
        try:
            materialName = data.get('materialName')
            importDate = data.get('importDate')
            amount = data.get('amount')
            material = Material.objects.get(materialName=materialName)
            Inventory.objects.create(material=material, importDate=importDate, importPack=amount)
        except Material.DoesNotExist:
            return JsonResponse({"success": False, "message": f"產品 {materialName} 不存在"})
        return JsonResponse({"success": True, "message": "更新成功"})


def getInventoryList(request):
    try:
        inventories = Inventory.objects.all().order_by('expiredDate')

        inventoryList = []
        for inventory in inventories:
            materialName = inventory.material.materialName
            inventoryData = {
                'id': inventory.id,
                'importPack': inventory.importPack,
                'importAmount': inventory.importAmount,
                'expiredDate': inventory.expiredDate,
                'materialName': materialName,
                'importDate': inventory.importDate,
            }
            inventoryList.append(inventoryData)

        return JsonResponse(inventoryList, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def updateInventory(request):
    if request.method == 'POST':
        # 從表單中獲取數據
        data = json.loads(request.body)
        try:
            inventoryID = data.get('id')
            print(inventoryID)
            inventory = Inventory.objects.get(id=inventoryID)
            materialName = data.get('materialName').strip()
            print(materialName)
            material = Material.objects.get(materialName=materialName)
            importPack = data.get('importPack')
            print(importPack)
            importDate = data.get('importDate')
            print(importDate)
            inventory.material = material
            inventory.importPack = importPack
            inventory.importDate = importDate
            inventory.save()
        except Material.DoesNotExist:
            return JsonResponse({"success": False, "message": f"產品 {materialName} 不存在"})
        return JsonResponse({"success": True, "message": "更新成功"})


def deleteInventory(request):
    if request.method == 'POST':
        inventoryID = request.POST.get("id")
        try:
            removeInventory(inventoryID=inventoryID)
            return JsonResponse({"success": True, "message": "資料刪除成功"})
        except Supplier.DoesNotExist:
            return JsonResponse({"success": False, "message": "訂單不存在"})


def getImportantList(request):
    try:
        importantList = []
        importants = Customer.objects.filter(segment="VIP")
        for important in importants:
            customerName = important.customerName
            customerPhone = important.customerPhone
            importantData = {'customerName': customerName, 'customerPhone': customerPhone}
            importantList.append(importantData)
        return JsonResponse(importantList, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def getNormalList(request):
    try:
        normalList = []
        normals = Customer.objects.filter(segment="Regular")
        for normal in normals:
            customerName = normal.customerName
            customerPhone = normal.customerPhone
            normalData = {'customerName': customerName, 'customerPhone': customerPhone}
            normalList.append(normalData)
        return JsonResponse(normalList, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def getDangerList(request):
    try:
        dangerList = []
        dangers = Customer.objects.filter(segment="At Risk")
        for danger in dangers:
            customerName = danger.customerName
            customerPhone = danger.customerPhone
            dangerData = {'customerName': customerName, 'customerPhone': customerPhone}
            dangerList.append(dangerData)
        return JsonResponse(dangerList, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def removeMaterial(materialID=None, material=None):
    if materialID is None:
        materialID = material.id
    elif material is None:
        try:
            material = Material.objects.filter(id=materialID)
        except Material.DoesNotExist:
            raise Material.DoesNotExist("找不到指定的產品")

    productList = []
    ingredients = Ingredient.objects.filter(material_id=materialID)
    if ingredients.exists():
        for ingredient in ingredients:
            product = Product.objects.filter(id=ingredient.product_id)
            productList.append(product)
    material.delete()
    if len(productList) > 0:
        for product in productList:
            removeProduct(product)


def removeSupplier(supplierID=None, supplier=None):
    if supplierID is None:
        supplierID = supplier.id
    elif supplier is None:
        try:
            supplier = Supplier.objects.filter(id=supplierID)
        except Supplier.DoesNotExist:
            raise Supplier.DoesNotExist("找不到指定的產品")

    materialList = []
    sources = MaterialSource.objects.filter(supplier_id=supplierID)
    if sources.exists():
        for source in sources:
            material = Material.objects.get(id=source.material_id)
            materialList.append(material)
    supplier.delete()
    if len(materialList) > 0:
        for material in materialList:
            removeMaterial(material)


def removeProduct(productID=None, product=None):
    if product is None:
        try:
            product = Product.objects.get(id=productID) # 取得單一物件
        except Product.DoesNotExist:
            raise Product.DoesNotExist("找不到指定的產品")
    elif productID is None:
        productID = product.id
    product.delete()


def removeCustomer(customerID=None, customer=None):
    if customer is None:
        try:
            customer = Customer.objects.get(id=customerID) # 取得單一物件
        except Customer.DoesNotExist:
            raise Product.DoesNotExist("找不到指定的客戶")
    elif customerID is None:
        customerID = customer.id
    customer.delete()


def removeOrder(orderID=None, order=None):
    if order is None:
        try:
            order = Order.objects.get(id=orderID) # 取得單一物件
        except Order.DoesNotExist:
            raise Product.DoesNotExist("找不到指定的訂單")
    elif orderID is None:
        orderID = order.id
    order.delete()


def removeInventory(inventoryID=None, inventory=None):
    if inventory is None:
        try:
            inventory = Inventory.objects.get(id=inventoryID) # 取得單一物件
        except Inventory.DoesNotExist:
            raise Inventory.DoesNotExist("找不到")
    elif inventoryID is None:
        inventoryID = inventory.id
    inventory.delete()


def getImportAmount(request):
    recurringOrders = Order.objects.filter(type="recurring"
                                          ).annotate(sellCount=F('mon') + F('tue') + F('wed') + F('thu') + F('fri'))

    recurringDict = defaultdict(list)
    for recurringOrder in recurringOrders:
        orderDetails = OrderDetail.objects.filter(order=recurringOrder)
        for orderDetail in orderDetails:
            ingredients = Ingredient.objects.filter(product=orderDetail.product)
            for ingredient in ingredients:
                recurringDict[ingredient.material.id].append(
                    int(orderDetail.amount) * int(ingredient.unit) * int(recurringOrder.sellCount)
                )

    now = datetime.now()
    oneMonthAgo = now - timedelta(days=30)
    oneTimeOrders = Order.objects.filter(type="oneTime", orderDate__gte=oneMonthAgo).order_by('-orderDate')
    if oneTimeOrders.count() < 20:
        oneTimeOrders = Order.objects.filter(type="oneTime", orderDate__lte=now).order_by('-orderDate')[:20]

    predictDict = defaultdict(list) # 每個 id 對應多個數據
    for oneTimeOrder in oneTimeOrders:

        orderDetails = OrderDetail.objects.filter(order=oneTimeOrder)
        for orderDetail in orderDetails:
            ingredients = Ingredient.objects.filter(product=orderDetail.product)
            for ingredient in ingredients:
                predictDict[ingredient.material.id].append(int(orderDetail.amount) * int(ingredient.unit))

    combinedDict = defaultdict(list)
    allID = set(recurringDict.keys()).union(predictDict.keys()) # 獲取所有的 id
    for materialID in allID:
        combinedDict[materialID] = recurringDict[materialID] + predictDict[materialID]

    stdDict = {}
    avgDict = {}
    for materialID, values in combinedDict.items():
        if len(values) > 1:
            stdDict[materialID] = statistics.stdev(values)
            avgDict[materialID] = statistics.mean(values)
        else:
            stdDict[materialID] = None
            avgDict[materialID] = None
    #服務水準95%，查表得Z=1.65
    Z = 1.65
    #10天訂一次，使用定期訂購模型
    OI = 10
    orderAmountDict = {}
    for materialID, values in stdDict.items():
        lt = Material.objects.get(id=materialID).shipDay
        inventoryAmount = Inventory.objects.filter(material_id=materialID).aggregate(totalImport=Sum('importAmount')
                                                                                    )['totalImport']
        packAmount = Material.objects.get(id=materialID).packAmount
        if inventoryAmount is None:
            inventoryAmount = 0
        quantity = avgDict[materialID] * (OI + lt) + Z * stdDict[materialID] * ((OI + lt) ** 0.5) - inventoryAmount
        if quantity > 0:
            quantity = math.ceil(quantity / packAmount)
        else:
            quantity = 0
        orderAmountDict[materialID] = quantity
    importList = []
    for key, value in orderAmountDict.items():
        supplier = MaterialSource.objects.get(material_id=key).supplier
        importData = {
            'materialName': Material.objects.get(id=key).materialName,
            'amount': value,
            'supplierName': supplier.supplierName,
            'supplierPhone': supplier.supplierPhone
        }
        importList.append(importData)
    return JsonResponse(importList, safe=False)


def refreshQuantity():
    now = datetime.now()
    lastRefresh = RefreshRecord.objects.all().order_by('-lastRefreshDate').first().lastRefreshDate
    startDate = lastRefresh.date()
    endDate = now.date()
    weekDayCount = Counter()
    currentDate = startDate
    while currentDate < endDate:
        weekDayCount[currentDate.weekday()] += 1
        currentDate += timedelta(days=1)
    recurringOrders = Order.objects.filter(type="recurring")

    recurringDict = defaultdict(int)
    for recurringOrder in recurringOrders:
        orderDetails = OrderDetail.objects.filter(order=recurringOrder)
        for orderDetail in orderDetails:
            ingredients = Ingredient.objects.filter(product=orderDetail.product)
            for ingredient in ingredients:
                if recurringOrder.mon == 1:
                    recurringDict[ingredient.material.id
                                 ] += int(orderDetail.amount) * int(ingredient.unit) * weekDayCount[0]

                elif recurringOrder.tue == 1:
                    recurringDict[ingredient.material.id
                                 ] += int(orderDetail.amount) * int(ingredient.unit) * weekDayCount[1]
                elif recurringOrder.wed == 1:
                    recurringDict[ingredient.material.id
                                 ] += int(orderDetail.amount) * int(ingredient.unit) * weekDayCount[2]
                elif recurringOrder.thu == 1:
                    recurringDict[ingredient.material.id
                                 ] += int(orderDetail.amount) * int(ingredient.unit) * weekDayCount[3]
                elif recurringOrder.fri == 1:
                    recurringDict[ingredient.material.id
                                 ] += int(orderDetail.amount) * int(ingredient.unit) * weekDayCount[4]
    oneTimeOrders = Order.objects.filter(type="oneTime", stored=False, orderDate__lte=now)

    oneTimeDict = defaultdict(int) # 每個 id 對應多個數據
    for oneTimeOrder in oneTimeOrders:
        print(oneTimeOrder.customer.customerName)
        orderDetails = OrderDetail.objects.filter(order=oneTimeOrder)
        for orderDetail in orderDetails:
            ingredients = Ingredient.objects.filter(product=orderDetail.product)
            for ingredient in ingredients:
                oneTimeDict[ingredient.material.id] += (int(orderDetail.amount) * int(ingredient.unit))
        oneTimeOrder.stored = True
        oneTimeOrder.save()
    combinedDict = defaultdict(int)
    allID = set(recurringDict.keys()).union(oneTimeDict.keys()) # 獲取所有的 id
    for materialID in allID:
        combinedDict[materialID] = recurringDict[materialID] + oneTimeDict[materialID]
    print(combinedDict)
    deductInventory(combinedDict)
    RefreshRecord.objects.create()


def deductInventory(materialDict):
    for key, value in materialDict.items():
        inventories = Inventory.objects.filter(material_id=key).order_by('importDate')
        remainAmount = int(value)
        with transaction.atomic():
            for inventory in inventories:
                importAmount = inventory.importAmount
                if remainAmount <= 0:
                    break

                if int(inventory.importAmount) > remainAmount:
                    importAmount -= remainAmount
                    remainAmount = 0
                    inventory.importAmount = importAmount
                    inventory.save()
                else:
                    remainAmount -= importAmount
                    inventory.delete()
        if remainAmount > 0:
            print(f"no {remainAmount}")


def getRFM():
    # 設定當前日期和週的日期
    analysisDate = datetime.now().date()
    currentWeek = {
        'mon': (analysisDate - timedelta(days=analysisDate.weekday())).isoformat(),
        'tue': (analysisDate - timedelta(days=analysisDate.weekday() - 1)).isoformat(),
        'wed': (analysisDate - timedelta(days=analysisDate.weekday() - 2)).isoformat(),
        'thu': (analysisDate - timedelta(days=analysisDate.weekday() - 3)).isoformat(),
        'fri': (analysisDate - timedelta(days=analysisDate.weekday() - 4)).isoformat(),
    }

    # 查詢一次性訂單 (oneTime orders)
    oneTimeRecency = Order.objects.filter(type="oneTime", customer_id=OuterRef('pk')).values('orderDate')[:1]

    # 查詢定期訂單 (recurring orders)
    recurringRecency = Order.objects.filter(type="recurring", customer_id=OuterRef('pk')).annotate(
        lastDeliveryDate=Case(
            When(mon=1, then=Value(currentWeek['mon'])),
            When(tue=1, then=Value(currentWeek['tue'])),
            When(wed=1, then=Value(currentWeek['wed'])),
            When(thu=1, then=Value(currentWeek['thu'])),
            When(fri=1, then=Value(currentWeek['fri'])),
            default=None,
            output_field=models.DateField()
        )
    ).values('lastDeliveryDate')[:1]
    defaultRecencyDate = analysisDate - timedelta(days=10)
    # 查詢所有顧客並計算 RFM 數據
    rfmData = Customer.objects.annotate(
        # 最近一次訂單距分析基準日期的天數 (Recency)
        recency=Coalesce(Subquery(oneTimeRecency), Subquery(recurringRecency), Value(defaultRecencyDate)),
        # 訂單次數 (Frequency)
        frequency=Count('orders'), # 使用 orders 來計算訂單數量
        # 總消費金額 (Monetary)
        monetary=Sum(F('orders__orderID__amount') * F('orders__orderID__product__productPrice')) # 使用 orders 來計算金額
    )

    # 計算 RFM 分數
    for customer in rfmData:
        recencyDate = customer.recency.date()
        recencyDays = (analysisDate - recencyDate).days
        recencyScore = 5 if recencyDays <= 2 else (
            4 if recencyDays <= 4 else (3 if recencyDays <= 6 else (2 if recencyDays <= 8 else 1))
        )
        frequencyScore = 5 if customer.frequency >= 8 else (
            4 if customer.frequency >= 6 else (3 if customer.frequency >= 4 else (2 if customer.frequency >= 2 else 1))
        )
        monetary = customer.monetary if customer.monetary is not None else 0
        monetaryScore = 5 if monetary >= 160 else (
            4 if monetary >= 120 else (3 if monetary >= 80 else (2 if monetary >= 40 else 1))
        )

        # 計算 RFM 分數
        rfmScore = f"{monetaryScore}{frequencyScore}{recencyScore}"
        rfmTotal = monetaryScore + frequencyScore + recencyScore
        # 根據 RFM 分數設定 Segment
        segment = ""
        if rfmTotal > 10:
            segment = "VIP"
        elif rfmTotal <= 10 and rfmTotal > 5:
            segment = "Regular"
        else:
            segment = "At Risk"

        customer.rfmScore = rfmScore
        customer.segment = segment
        customer.save()
