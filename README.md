# Cистема управления заказами в кафе
Это полнофункциональное веб-приложение на Django для управления заказами в кафе. Оно позволяет добавлять, удалять, искать, изменять и отображать заказы через веб-интерфейс.
Пользователь может добавлять и удалять заказ, осуществлять его поиск по номеру стола или статусу через поисковую строку, отображать список всех заказов, а также менять их статусы (“в ожидании”, “готово”, “оплачено”). Есть возможность посмотреть общий объём выручки за заказы со статусом “оплачено”. Кроме того реализована возможность редактирования заказа (добавление или удаление позиций), а также фильтрация списка заказов по статусу.
Для хранения данных использована база данных PostgreSQL.

## Инструкция по развертыванию проекта
1.	Клонируйте репозиторий в папку
   ```git clone https://github.com/examplesOfWorks/cafe.git```
2.	В этой же папке установите виртуальное окружение и активируйте его
```python -m venv venv```
venv\Scripts\activate.bat
3.	Перенесите из папки cafe папку с виртуальным окружением файл ```requirements.txt```. Затем установите зависимости
```pip install -r requirements.txt```
4.	Перейдите в папку cafe
```cd cafe```
5.	Создайте базу данных в PostgreSQL
6.	В папке с настойками проекта в файле ```db_secret.py``` сохраните в переменные NAME, USER и PASSWORD название базы данных, имя пользователя и пароль от неё соответственно по предоставленному примеру. 
7.	Запустите миграции
```python manage.py makemigrations```
```python manage.py migrate```
8.	Создайте администратора
```python manage.py createsuperuser```
9.	Запустите сервер
```python manage.py runserver```
10.	Откройте браузер и перейдите по адресу ```http://127.0.0.1:8000/```. Можно начинать работу с заказами. 


