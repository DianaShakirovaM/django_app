# Django Tree Menu — древовидное меню

[![Django](https://img.shields.io/badge/Django-≥3.2-brightgreen.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-≥3.8-blue.svg)](https://www.python.org/)

## Основные возможности

1. Меню реализовано через **template tag**   
2. Хранится в БД  
3. Полностью редактируется в стандартной **админке Django**  
4. Активный пункт определяется по текущему URL (поддержка named URL)  
5. На одной странице может быть **несколько меню** — задаются по имени  
6. Поддержка явных URL и **named URL** (с подстановкой параметров текущего view)  
7. **Ровно 1 запрос к БД** на отрисовку любого меню  

## Установка
1. Склонировать репозиторий
```bash
git clone https://github.com/DianaShakirovaM/django_app
```
2. Создать виртуальное окружение
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```
3. Установить зависимости
```bash
pip install -r requirements.txt
```
4. Выполнить миграции
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Создать суперпользователя
```bash
python manage.py createsuperuser
```
6. Запустить сервер
```bash
python manage.py runserver
```

## Использование
В любом шаблоне:
```bash
{% load draw_menu %}

{% draw_menu 'main_menu' %}
{% draw_menu 'sidebar_menu' %}
{% draw_menu 'footer_menu' %}
```
