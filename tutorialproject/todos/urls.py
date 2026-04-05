from django.urls import path

from todos import views

urlpatterns = [
    path("hello", views.hello_world_view, name="hello_world"),
    path("", views.hello_html_view, name="hello_default"),
    path("hello_html", views.hello_html_view, name="hello_html"),
    path("hello_path/<str:name>", views.hello_path, name="hello_path"),
    path("hello_query", views.hello_query, name="hello_query"),
    path("redirect_view", views.redirect_view, name="redirect_view"),
    path("post_example", views.post_example, name="post_example"),
    path("submit_example", views.submit_example, name="submit_example"),
    path("submit_django_form", views.submit_django_form, name="submit_django_form"),
    path("template_view", views.template_view, name="template_view"),
    path("todos", views.todos, name="todos"),
    path("delete_todo/<int:todo_id>", views.delete_todo, name="delete_todo"),
    path("toggle_todo/<int:todo_id>", views.toggle_todo_done, name="toggle_todo"),
    path("person/<int:person_id>", views.person_details, name="person_details"),
]
