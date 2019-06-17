
## Steps
- start app
    ```
    # (cd to the directory where the manage.py file is)
    $ django-admin startapp my_new_app 
    ```
 - include the "a_new_app" in INSTALLED_APPS in settings.py
    ```python
    INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
    
       'my_new_app',
    ]
    ```
 - setup a url for my_new_app in urls.py: 
    ```python
    urlpatterns = [
        path('my_new_feature/', views.my_new_feature, name='my_new_feature'),
        path('admin/', admin.site.urls),
    ]
    ```
 - create a new function in my_new_app/views.py:
    ```python
    def my_new_feature(request):
       return render(request, 'my_new_feature.html')
    ```
 - implement the templates/my_new_feature.html
 - write tests for new feature in my_new_app/tests.py
 - run and fail tests
 - implement my_new_feature in my_new_app/views.py and models for it in my_new_app/models.py
 - run and pass tests
    
## commands
- start a new django project: 
    ```
    $ django-admin startproject myproject
    ```
- start a new app: 
    ```
    (cd to the directory where the manage.py file is)
    $ django-admin startapp boards
    ```
- run server: 
    ```
    $ python manage.py runserver
    ```
- migrate for changes in models:
    ```
    $ python manage.py makemigrations
    ```
- apply migrations we generated to the database: 
    ```
    $ python manage.py migrate
    ```
- enter to interactive shell with django: 
    ```
    $ python manage.py shell
    ```
- run tests:
    ```
    $ python manage.py test
    ```
  
