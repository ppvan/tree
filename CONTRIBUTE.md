# Table of Contents
- [Table of Contents](#table-of-contents)
  - [References](#references)
  - [Django commands](#django-commands)
    - [Create project](#create-project)
    - [Create app](#create-app)
    - [Run server](#run-server)
    - [Create migration](#create-migration)
    - [Apply migration](#apply-migration)
    - [Create superuser](#create-superuser)
    - [Run tests](#run-tests)
  - [Examples](#examples)
    - [A dead simple view](#a-dead-simple-view)
    - [A view with template](#a-view-with-template)
    - [Start tailwindcss](#start-tailwindcss)


<br />
<br />

## References
- [Concurency problems](https://docs.djangoproject.com/en/4.1/ref/models/expressions/#avoiding-race-conditions-using-f)
- [Django Generic Views](https://docs.djangoproject.com/en/4.1/topics/class-based-views/)
- [Django Request and Response](https://docs.djangoproject.com/en/4.1/ref/request-response)
- [Templates](https://docs.djangoproject.com/en/4.1/topics/templates/)
- [Django shortcuts](https://docs.djangoproject.com/en/4.1/topics/http/shortcuts/)


## Django commands

### Create project
```bash
django-admin startproject <project-name> # create project
```

### Create app
```bash
python manage.py startapp <app-name> # create app
```

### Run server
```bash
python manage.py runserver
```
> Restart server, port 8000 is used

### Create migration
```bash
python manage.py makemigrations
```
>Create migration SQL file (when you make change to models, rerun this command)

### Apply migration
```bash
python manage.py migrate
```
>Apply migration (from SQL to database)

### Create superuser
```bash
python manage.py createsuperuser
```
### Run tests
```bash
python manage.py test <app-name>
```

## Examples

### A dead simple view
```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

### A view with template
```python
from django.shortcuts import render

def index(request):
    context = {
        'title': 'Home',
        'content': 'Welcome to the home page',
    }

    return render(request, 'index.html', context)
```

### Start tailwindcss
```bash
./tailwindcss -i ./static/tailwind.css -o ./static/output.css --watch
```