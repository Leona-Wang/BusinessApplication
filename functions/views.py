from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def showBOM(request):
    return render(request, 'showBOM.html')


def addBOM(request):
    return render(request, 'addBOM.html')


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
