# BusinessApplication
html檔案最前面加{% load static %}
調用static資料夾內檔案：{% static '相對路徑' %}
ex：{% static 'vendor/fontawesome-free/css/all.min.css' %}
run server：python manage.py runserver
修改/新增資料庫：
1.python manage.py makemigrations
2.python manage.py migrate
叫 django shell：python manage.py shell