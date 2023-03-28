## Django notes

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