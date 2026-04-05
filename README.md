# Django Full Crash Course
Created Wednesday 01 April 2026

Overview
--------
YouTube: <https://www.youtube.com/watch?v=u1GnZfDw5LU>

Setup
-----
create virtual environment
``pyenv virtualenv 3.13.1 django``

set local python
``pyenv local django``

install django
``pip install django``

Django Project
--------------
Create django project
``django-admin startproject core tutorialproject``

Structure of empty project
``.``
``└── tutorialproject``
``├── core``
``│   ├── asgi.py``
``│   ├── __init__.py``
``│   ├── settings.py``
``│   ├── urls.py``
``│   └── wsgi.py``
``└── manage.py``

Enter project directory
``cd tutorialproject``

Django App/Module
-----------------
It's recommended to split our project into modules using django app.

Create new django app (inside project directory)
``django-admin startapp todos``

Django App structure
	└── todos
	    ├── admin.py
	    ├── apps.py
	    ├── __init__.py
	    ├── migrations
	    │   └── __init__.py
	    ├── models.py
	    ├── tests.py
	    └── views.py

Create Simple View
------------------
Create handler function
``tutorialproject/todos/views.py``
	from django.http import HttpResponse
	
	# Create your views here.
	def hello_world_view(request):
	    return HttpResponse(b'Hello, World!')

Add handler url
``tutorialproject/todos/urls.py``
	from django.urls import path
	
	from todos import views
	
	urlpatterns = [
	    path('hello', views.hello_world_view, name='hello_world'),
	]

Add to project urls
``tutorialproject/core/urls.py``
	from django.contrib import admin
	from django.urls import include, path
	
	urlpatterns = [
	    path('admin/', admin.site.urls),
	    path('', include('todos.urls'))
	]

Add app to project
``tutorialproject/core/settings.py``
	INSTALLED_APPS = [
	    'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.messages',
	    'django.contrib.staticfiles',
	    'todos'
	]

Run development server
----------------------
Run project for development
``python manage.py runserver``

Open url on browser
``http://127.0.0.1:8000/hello``

Render HTML View
----------------
Create handler
``tutorialproject/todos/views.py``
	def hello_html_view(request):
	    return render(request, 'todos/hello.html')

Create html template
``tutorialproject/todos/templates/todos/hello.html``
	<!DOCTYPE html>
	<html lang="en">
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>Hello</title>
	</head>
	<body>
	    <h1>Hello!</h1>
	</body>
	</html>

Add handler url
``tutorialproject/todos/urls.py``
	urlpatterns = [
	    path('hello_html', views.hello_html_view, name='hello_html'),
	]

Path Variable
-------------
Create handler
``tutorialproject/todos/views.py``
	def hello_path(request, name):
	    return HttpResponse(f'Hello, {name}!'.encode())

Add handler url
``tutorialproject/todos/urls.py``
	urlpatterns = [
	    path("hello_path/<str:name>", views.hello_path, name="hello_path"),
	]

Query Param
-----------
Create handler
``tutorialproject/todos/views.py``
	def hello_query(request):
	    return HttpResponse(f'Hello, {request.GET.get("name")}!'.encode())

Add handler url
``tutorialproject/todos/urls.py``
	urlpatterns = [
	    path("hello_query", views.hello_query, name="hello_query"),
	]

Call URL with query param
``http://127.0.0.1:8000/hello_query?name=ZEN``

Redirect Request
----------------
Create handler
``tutorialproject/todos/views.py``
	def redirect_view(request):
	    return redirect("hello_html")

Add handler url
``tutorialproject/todos/urls.py``
	urlpatterns = [
	    path("redirect_view", views.redirect_view, name="redirect_view"),
	]

Call URL with query param
``http://127.0.0.1:8000/redirect_view``

POST Request
------------
Create handler
``tutorialproject/todos/views.py``
	def post_example(request):
	    if request.method == "POST":
	        name = request.POST.get("name")
	        age = request.POST.get("age")
	        job = request.POST.get("job")
	
	        return HttpResponse(
	            f"Hello, {name}! You are {age} years old. You work as a {job}.".encode()
	        )
	    else:
	        return HttpResponseNotAllowed(["POST"])

Add handler url
``tutorialproject/todos/urls.py``
	urlpatterns = [
	    path("post_example", views.post_example, name="post_example"),
	]

Call URL with query param
``http://127.0.0.1:8000/post_example``
Response 405 Method Not Allowed

Add submit form handler
``tutorialproject/todos/views.py``
	def submit_example(request):
	    return render(request, "todos/submit.html")

Create submit html template 
	<html>
	    <body>
	        <form method="POST" action="{% url 'post_example' %}">
	            {% csrf_token %}
	            <input type="text" name="name" placeholder="Name">
	            <input type="text" name="age" placeholder="Age">
	            <input type="text" name="job" placeholder="Job">
	            <button type="submit">Submit</button>
	        </form>
	    </body>
	</html>

Add handler url
``tutorialproject/todos/urls.py``
	urlpatterns = [
	    path("submit_example", views.submit_example, name="submit_example"),
	]

Open submit form
``http://127.0.0.1:8000/submit_example``
fill form and submit to send POST request

Django Form
-----------
Create django form class
``todos/forms.py``
	from django import forms
	
	class PersonForm(forms.Form):
	    name = forms.CharField(max_length=100, required=True, label="Your Name")
	    age = forms.IntegerField(required=True, label="Your Age")
	    job = forms.CharField(required=False, label="Your Job")

Create submit django form handler
``tutorialproject/todos/views.py``
	def submit_django_form(request):
	    form = PersonForm()
	    return render(request, "todos/submit_django_form.html", {"form": form})

Create submit html template 
	<html>
	    <body>
	        <form method="POST" action="{% url 'post_example' %}">
	            {% csrf_token %}
	            {{ form.as_p }}
	            <button type="submit">Submit</button>
	        </form>
	    </body>
	</html>

Add handler url
``tutorialproject/todos/urls.py``
	urlpatterns = [
	    path("submit_django_form", views.submit_django_form, name="submit_django_form"),
	]

Modify POST handler to use django form
``tutorialproject/todos/views.py``
	def post_example(request):
	    if request.method == "POST":
	        form = PersonForm(request.POST)
	        if form.is_valid():
	            name = form.cleaned_data.get("name")
	            age = form.cleaned_data.get("age")
	            job = form.cleaned_data.get("job")
	
	            return HttpResponse(
	                f"Hello, {name}! You are {age} years old. You work as a {job}.".encode()
	            )
	
	    return HttpResponseNotAllowed(["POST"])

Open submit form
``http://127.0.0.1:8000/submit_django_form``
fill form and submit to send POST request

Django Templates
----------------
Render can optionally use context to send data to templates.
``tutorialproject/todos/views.py``
``def template_view(request):``
``context = {``
``"name": "Zen",``
``"age": 333,``
``"skills": [``
``"Software Engineer",``
``"Python Developer",``
``# "Java",``
``"Rust",``
``],``
``}``
``return render(request, "todos/template_demo.html", context)``

The context data then can be used in template to dynamically render html page.
``todos/templates/todos/template_demo.html``
	<html lang="en">
	    <head>
	        <meta charset="UTF-8" />
	        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
	        <title>Document</title>
	    </head>
	    <body>
	        <h1>{{ name }}</h1>
	        <h1>{{ age }}</h1>
	        <h1>{{ skills }}</h1>
	        <ul>
	            {% for skill in skills %}
	            <li>{{ skill }}</li>
	            {% endfor %}
	        </ul>
	        {% if skills|length > 3 %}
	        <p>{{name}} has alot of skills</p>
	        {% elif 'Rust' in skills %}
	        <p>{{name}} is awesome</p>
	        {% endif %}
	    </body>
	</html>

Template directives:

* Core Syntax
	* Variables: ``{{ variable_name }}`` — Displays a value from the context.
	* Tags: {% tag_name %} — Performs logic like loops or includes.
	* Filters: ``{{ variable|filter_name }}``— Modifies the display of a variable.
	* Comments: ``{# comment #}`` — Notes that are not rendered in the final HTML. 
* Essential Template Tags
	* Inheritance & Layout:
		* {% extends "base.html" %}: Specifies a parent template that this template inherits from.
		* {% block title %}{% endblock %}: Defines a section that child templates can override.
		* {% include "sidebar.html" %}: Loads another template into the current one.
	* Control Flow:
		* {% if user.is_authenticated %}...{% endif %}: Standard conditional logic.
		* {% for item in list %}...{% endfor %}: Iterates over a collection.
	* Utility:
		* {% load static %}: Loads custom template tag libraries, most commonly for static files.
		* {% url 'view_name' %}: Generates a URL for a specific view.
		* {% csrf_token %}: Protects against Cross-Site Request Forgery in forms.
* Advanced & Utility Tags
	* {% with %}: Caches a complex variable under a simpler name for use within the block.
	* {% cycle %}: Alternates between a list of values each time it is encountered, often used for zebra-striping table rows.
	* {% verbatim %}: Prevents Django from rendering the contents of the tag, which is useful when using JavaScript frameworks like Vue or Angular that use similar syntax.
	* {% autoescape %}: Manually controls the HTML auto-escaping behavior for a block of text.
	* {% now %}: Displays the current date and time using a specified format string.
	* {% comment %}: Ignores everything within the tag, allowing for multi-line developer notes that won't appear in the rendered HTML source.


Add handler url
``tutorialproject/todos/urls.py``
	urlpatterns = [
	    path("template_view", views.template_view, name="template_view"),
	]

Base template is useful to provide common page structure for other pages.
``todos/templates/todos/base.html``
	<!doctype html>
	<html>
	    <head>
	        <meta charset="UTF-8" />
	        <title>{% block title %}Page Title{% endblock %}</title>
	    </head>
	    <body>
	        <header>
	            <h1>{% block header %}Page Header{% endblock %}</h1>
	        </header>
	        <main>{% block content %}Content{% endblock %}</main>
	        <footer>Copyright ByMe &copy; 2026</footer>
	    </body>
	</html>

Use base template
``todos/templates/todos/template_demo.html``
	{% extends 'todos/base.html' %}
	
	{% block title %}Template Demo{% endblock %}
	
	{% block header %}Template Demo{% endblock %}
	
	{% block content %}
	<h1>{{ name }}</h1>
	<h1>{{ age }}</h1>
	<h1>{{ skills }}</h1>
	<ul>
	    {% for skill in skills %}
	    <li>{{ skill }}</li>
	    {% endfor %}
	</ul>
	{% if skills|length > 3 %}
	<p>{{name}} has alot of skills</p>
	{% elif 'Rust' in skills %}
	<p>{{name}} is awesome</p>
	{% endif %}
	{% endblock %}

Database Model & Migration
--------------------------
Create Model
``todos/models.py``
	from django.db import models
	
	
	class PriorityChoices(models.IntegerChoices):
	    LOW = 0, 'Low'
	    MEDIUM = 1, 'Medium'
	    HIGH = 2, 'High'
	
	
	class Todo(models.Model):
	    title = models.CharField(max_length=100)
	    description = models.CharField(max_length=500)
	    done = models.BooleanField(default=False)
	    deadline = models.DateTimeField(null=True, blank=True)
	    priority = models.IntegerField(
	        choices=PriorityChoices.choices, null=True, blank=True)
	
	    def __str__(self):
	        return f"{self.id} - {self.title}"

Create Form Model
``todos/forms.py``
	class TodoForm(forms.ModelForm):
	    class Meta:
	        model = Todo
	        fields = ["title", "description", "done", "deadline", "priority"]
	
	        widgets = {
	            "deadline": forms.DateInput(attrs={"type": "date"}),
	        }

Create handler
``tutorialproject/todos/views.py``
	def todos(request):
	    if request.method == "POST":
	        form = TodoForm(request.POST)
	        
	        if form.is_valid():
	            todo = form.save()
	            return HttpResponse("Todo created successfully!".encode())
	    else:
	        form = TodoForm()
	        todos = Todo.objects.all()
	        return render(request, "todos/todos.html", {"form": form, "todos": todos}

Add handler url
``tutorialproject/todos/urls.py``
	urlpatterns = [
	    path("todos", views.todos, name="todos"),
	]

Create template
``todos/templates/todos/todos.html``
	{% extends 'todos/base.html' %}
	
	{% block title %}Todos{% endblock %}
	
	{% block header %}Todos{% endblock %}
	
	{% block content %}
	<ul>
	    {% for todo in todos %}
	    <li><b>{{ todo.id }} - {{ todo.title }}</b> (Done: {{todo.done}})</li>
	    {% endfor %}
	</ul>
	
	<form method="post">
	    {% csrf_token %}
	    {{ form.as_p }}
	    <button type="submit">Create Todo</button>
	</form>
	{% endblock %}

Create migration
``python manage.py makemigrations``

Perform migration
``python manage.py migrate``

Add Person model and add field owner on Todo
``todos/models.py``
	class Person(models.Model):
	    name = models.CharField(max_length=100)
	    age = models.IntegerField()
	
	    def __str__(self):
	        return f"{self.id} - {self.name}"

	class Todo(models.Model):
	
	    owner = models.ForeignKey(
	        Person, on_delete=models.CASCADE, related_name="todos", blank=True, null=True

Add owner on todos template
``todos/templates/todos/todos.html``
	<ul>
	    {% for todo in todos %}
	    <li><b>{{ todo.id }} - {{ todo.title }}</b> (Done: {{todo.done}}) (Owned by: {{ todo.owner.name }})</li>
	    {% endfor %}
	</ul>

Create migration
``python manage.py makemigrations``

Perform migration
``python manage.py migrate``

Add person detail handler
``tutorialproject/todos/views.py``
	def person_details(request, person_id):
	    person = Person.objects.filter(id=person_id).first()
	
	    return render(request, "todos/person_details.html", {"person": person})

Add handler to urls
``tutorialproject/todos/urls.py``
	urlpatterns = [
	    path("person/<int:person_id>", views.person_details, name="person_details"),
	]

Add person detail template
``todos/templates/todos/person_details.html``
	{% extends 'todos/base.html' %}
	
	{% block title %}{{ person.name }} Details{% endblock %}
	
	{% block header %}{{ person.name }} Details{% endblock %}
	
	{% block content %}
	<h1>Hello, {{ person.name }}</h1>
	<h3>Your Todos</h3>
	<ul>
	    {% for todo in person.todos.all %}
	    <li>{{ todo.id }} - {{ todo.title }} (Done: {{todo.done}})</li>
	    {% endfor %}
	</ul>
	{% endblock %}

Add delete todo handler and toggle todo done handler
``tutorialproject/todos/views.py``
``def delete_todo(request, todo_id):``
``Todo.objects.filter(id=todo_id).delete()``
	
``return HttpResponse("Todo deleted successfully!".encode())``
		
``def toggle_todo_done(request, todo_id):``
``todo = Todo.objects.filter(id=todo_id).first()``
	
``if todo:``
``todo.done = not todo.done``
``todo.save()``
	
``return HttpResponse("Todo done status updated successfully!".encode())``

Add handlers to urls
``tutorialproject/todos/urls.py``
	urlpatterns = [
	    path("delete_todo/<int:todo_id>", views.delete_todo, name="delete_todo"),
	    path("toggle_todo_done/<int:todo_id>", views.toggle_todo_done, name="toggle_todo_done"),
	]

Call url to toggle todo 
``http://127.0.0.1:8000/toggle_todo/1``

Call url to delete todo
``http://127.0.0.1:8000/delete_todo/3``

Django Admin Panel
------------------
Create superuser first to use admin panel
``python manage.py createsuperuser``
Username: admin
Email address: [admin@mail.com](mailto:admin@mail.com)
Password: admin

Open admin panel
``http://127.0.0.1:8000/admin``

Login as admin
username: admin
password: admin

Admin will show only Authentication and Authorization models
We need to add our model to administration panel

Add our model to admin panel
``todos/admin.py``
	from todos.models import Person, Todo
	
	admin.site.register(Todo)
	admin.site.register(Person)

Now our model will registered and can be managed in admin panel
Add person and update todo with owner using admin panel

Show the new person detail
``http://127.0.0.1:8000/person/1``

Customize admin panel model
---------------------------
We can customize admin model such as field list, add search and filter
``todos/admin.py``
	from django.contrib import admin
	
	from todos.models import Person, Todo
	
	# admin.site.register(Todo)
	admin.site.register(Person)
	
	
	@admin.register(Todo)
	class TodoAdmin(admin.ModelAdmin):
	    list_display = ('title', 'priority', 'deadline', 'done')
	    list_filter = ('deadline', 'priority')
	    search_fields = ('title',)

Now the admin panel for Todo will change according to the custom model admin


Django shell
------------
We can also use django shell to interact with database
``python manage.py shell``
	>>> from todos.models import *
	>>> Todo.objects.all()
	<QuerySet [<Todo: 1 - Task 1>, <Todo: 2 - Task 2>]>
	>>> Todo.objects.filter(owner__name='Zero')
	<QuerySet [<Todo: 2 - Task 2>]>
	>>> Todo.objects.filter(owner__name='Zero').first()
	<Todo: 2 - Task 2>
	>>> 


Static files
------------
We can serve static file with django
Modify settings file
``core/settings.py``
	# Static files (CSS, JavaScript, Images)
	# https://docs.djangoproject.com/en/6.0/howto/static-files/
	
	STATIC_URL = 'static/'
	STATICFILES_DIRS = [BASE_DIR / "static"]

Create static directory in our root project directory
We can store our static files inside this directory

Add static urls
``core/urls.py``
	from django.conf.urls.static import static
	from django.conf import settings
	
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

Now static file inside ``static`` directory can be accessed from [``/static``](file:///static) prefix URL.

Use static css file inside out base template html
``todos/templates/todos/base.html``
	
Make css file
``static/css/style.css``
	body {
	    background-color: cyan;
	}


Manually edit migration
-----------------------
Sometime django make migration cannot detect the change correctly
In this case we can edit migration script manually
For example we rename column name and add secondary index

Gunicorm & Postgresql with Docker
---------------------------------
For deployment we can use Gunicorn as web server and postgresql as database. Also use docker for container deployment. 

Install gunicorn
``pip install gunicorn``

Run our project with gunicorn
``gunicorn core.wsgi:application``

Django static file url may error when served via gunicorn. 
To fix this we can use WhiteNoise package.

Install whitenoise
``pip install whitenoise``

Add whitenoise middleware by modifying settings file
``core/settings.py``
``MIDDLEWARE = [``
``# ...``
'``whitenoise.middleware.WhiteNoiseMiddleware',``
``]``

Postgresql connection setting
``core/settings.py``
	DATABASES = {
	    'default': {
	'ENGINE': 'django.db.backends.postgresql',
	'NAME': 'postgres',
	'USER': 'postgres',
	'PASSWORD': 'postgres',
	'HOST': 'localhost',
	'POST': 5432,
	    }
	}

Install postgresql driver package
``pip install psycopg2-binary``


Settings
--------
To manage Django settings across development, staging, and production environments, the most widely accepted best practice is
a modular settings structure combined with environment variables for secrets

### 1. Modular Settings Structure
Instead of a single settings.py, create a settings/ directory to house environment-specific files.
Recommended Directory Structure:
	my_project/
	└── config/
	    ├── settings/
	    │   ├── __init__.py
	    │   ├── base.py          # Shared settings (INSTALLED_APPS, MIDDLEWARE)
	    │   ├── development.py   # Local dev settings (DEBUG=True, SQLite)
	    │   ├── staging.py       # Staging settings (DEBUG=False, mirror Prod)
	    │   └── production.py    # Production settings (DEBUG=False, Secure DB)
	    └── wsgi.py


* base.py: Contains all common configuration. Update BASE_DIR to account for the extra folder level: ``BASE_DIR = Path(__file__).resolve().parent.parent.parent.``
* Environment Files: Each file imports everything from base and overrides only what is necessary:

	# settings/development.py
	from .base import *
	DEBUG = True
	# ... other dev overrides
### 2. Use Environment Variables for Secrets
Never hardcode sensitive data like SECRET_KEY, database passwords, or API keys in your settings files. Use libraries like django-environ or python-decouple to load them from a .env file or the system environment. 

* Exclude .env: Always add .env to your .gitignore to prevent leaking secrets to version control. 


### 3. Loading the Correct Environment
Tell Django which settings module to use by setting the DJANGO_SETTINGS_MODULE environment variable.
``Task 	        Command``
``Development	export DJANGO_SETTINGS_MODULE=config.settings.development``
``Staging	        export DJANGO_SETTINGS_MODULE=config.settings.staging``
``Production	export DJANGO_SETTINGS_MODULE=config.settings.production``

You should also update the default values in manage.py, wsgi.py, and asgi.py to point to your development settings so that local commands work without extra flags. 

### 4. Staging vs. Production Differences
A staging environment should mirror production as closely as possible to catch deployment issues early. 

* Mirroring: Use the same database engine (e.g., PostgreSQL) and caching backend.
* Data: Use anonymized or synthetic data instead of real production user data for security.
* Security: Enable HTTPS and security headers (SECURE_SSL_REDIRECT, SESSION_COOKIE_SECURE) in staging just as you would in production. 


### 5. Othres
To deploy a Django application securely and efficiently, you must update several critical settings in your settings.py file to transition from a development environment to a production one. 

#### 1. Critical Security Settings
These are the most vital changes to prevent unauthorized access and data leaks: 

* DEBUG = False: Never run a production site with DEBUG = True. This prevents the exposure of sensitive stack traces and configuration details to users.
* SECRET_KEY: This must be a large, random value and kept strictly confidential. Use environment variables to load it rather than hardcoding it in your repository.
* ALLOWED_HOSTS: Define the specific domain names or IP addresses that can serve your Django app (e.g., ['[www.yourdomain.com](www.yourdomain.com)', '12.34.56.78']) to prevent HTTP Host header attacks. 


#### 2. Database and Static Files
Production environments require more robust handling of data and assets than the default development server. 

* DATABASES: Switch from SQLite to a production-ready database like PostgreSQL or MySQL. Use environment variables for credentials.
* STATIC_ROOT: Define the absolute path where python manage.py collectstatic will gather all your static files for your web server (like Nginx) to serve.
* STATIC_URL: Ensure this is set correctly (usually '/static/') for the web server to locate your assets. 


#### 3. HTTPS and Security Headers
For production, you should force secure connections and enable protective headers: 

* SECURE_SSL_REDIRECT = True: Redirects all non-HTTPS requests to HTTPS.
* SESSION_COOKIE_SECURE = True: Ensures cookies are only sent over HTTPS.
* CSRF_COOKIE_SECURE = True: Protects CSRF tokens by ensuring they are only transmitted over secure connections. 


#### 4. Recommended Environment Structure
A common best practice is to split your settings into multiple files to manage different environments easily. 
``File 	        Purpose``
``base.py	        Settings common to both local and production (e.g., INSTALLED_APPS).``
``local.py	Development-specific settings like DEBUG = True and internal databases.``
``production.py	Deployment settings like DEBUG = False, production DB, and security headers.``

#### Summary Checklist for Deployment

* Check Configuration: Run python manage.py check --deploy to identify missing security settings.
* Environment Variables: Use tools like python-dotenv or django-environ to keep secrets out of version control.
* Production Server: Use a WSGI server like Gunicorn or uWSGI instead of runserver.
* Static Files: Run python manage.py collectstatic to prepare assets for your web server. 


Setting from Environment Variables
----------------------------------
To get setting values from environment variables in Django, you can use the built-in
os.environ module or a dedicated library like django-environ or python-decouple. 

### 1. Using Built-in os.environ (No Extra Libraries)
The standard way is to use Python's os module. It is simple but only handles strings, so you must manually cast types like booleans or integers. 

* ``os.environ.get('VAR', default)``: Recommended as it prevents the app from crashing if a variable is missing by returning a default value.
* ``os.environ['VAR']``: Use this if the variable is mandatory. It will raise a KeyError if the variable is missing. 


Sample:
``import os``
	
``# Example usage in settings.py``
``SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key-for-dev-only')``
``DEBUG = os.environ.get('DEBUG', 'False') == 'True'  # Manual boolean casting``


### 2. Using django-environ (Recommended for Projects)
This library is widely used because it automatically handles type casting (booleans, integers, lists) and can parse complex strings like database URLs. 
Install: ``pip install django-environ``.
Setup in settings.py:
``import environ``
``import os``

``env = environ.Env(``
``# Set default values and types``
``DEBUG=(bool, False)``
``)``

``# Read .env file if it exists``
``environ.Env.read_env(os.path.join(BASE_DIR, '.env'))``

``# Access variables``
``DEBUG = env('DEBUG')  # Automatically cast to boolean``
``SECRET_KEY = env('SECRET_KEY')``
``DATABASES = {``
'``default': env.db(), # Automatically parses DATABASE_URL``
``}``

### 3. Comparison of Common Methods
``Method 	        Type Casting	.env File Support  Best For``
``os.environ	Manual	        No	           Small projects, minimal dependencies.``
``django-environ	Automatic	Yes	           Standard Django projects, complex DB/Cache setups.``
``python-decouple	Automatic	Yes	           Projects needing strict separation of config and code.``

### Important Security Note
Always add your .env file to your .gitignore to ensure sensitive keys are never committed to your version control system. 


