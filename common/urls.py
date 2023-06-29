from django.urls import path
from django.contrib.auth import views as auth_views
from common.views import index, signup, login, password_reset_request, social_signup, social_signup_complete

app_name = 'common'

urlpatterns = [
    path('',
    index,
    name = 'index'
    ),
    path(
        'login/', 
        login, 
        name = 'login'
        ),
    path(
        'logout/', 
        auth_views.LogoutView.as_view(), 
        name = 'logout'
        ),
    path(
        'signup/',
        signup,
        name = 'signup',
    ),
    #template_named을 as_view의 인자로 
    path("password_reset/", password_reset_request, name="password_reset"),
    # path("accounts/social/signup/", social_signup, name = "social_signup"),
    path("social-signup-copmlete/", social_signup_complete, name = "social_signup_complete")
]
