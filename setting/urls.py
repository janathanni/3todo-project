from django.urls import path
from django.contrib.auth import views as auth_views
from setting.views import setting, set_password, resign, set_username, agreements

app_name = 'setting'

urlpatterns = [
    path('', setting, name = "settings" ), 
    path('set-password/', set_password, name = 'set-password'),
    path('resign/', resign, name = "resign"),
    path('set-username/', set_username, name = "set-username"),
    path('agreements', agreements, name = 'agreements')
    
]