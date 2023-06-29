from django.urls import path
from django.contrib.auth import views as auth_views
from todo.views import add_todo, update_todo, delete_todo, todo, donelist

app_name = 'todo'

urlpatterns = [
    path('', todo, name = "todo"), #오늘 할 일 목록을 보여주는 url 
    path('donelist/', donelist, name = "donelist" ), #지금까지 해온 일들을 보여주는 url 
    path('add/', add_todo, name = "add"),
    path('update/<int:todo_id>', update_todo, name = "update"),
    path('delete/<int:todo_id>', delete_todo, name = "delete"),
]