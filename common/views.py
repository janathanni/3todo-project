from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from common.forms import UserCreationForm, LoginForm
from common.models import User
from django.contrib.auth import login as auth_login
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.template import loader
from allauth.socialaccount.views import SignupView

def index(request):
    if request.user.is_authenticated:
        return redirect('/todo')

    return render(request, 'common/index.html')

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request = request, email = email, password = password)

            #user일 때
            if user is not None:
                auth_login(request, user)
                return redirect('todo:todo')
            
            #user가 아닐 때
            else:
                form.add_error('email', '이메일 혹은 비밀번호가 틀렸습니다.')

    else:
        form = LoginForm()
    
    return render(request, 'common/login.html', {'form' : form})

def signup(request):
    if request.method == "POST" :
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'common/signup_success.html')
    else:
        form = UserCreationForm()

    return render(request, 'common/signup.html', {'form':form})

# #https://ordinarycoders.com/blog/article/django-password-reset
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            print(associated_users)
            if associated_users:
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': '3todo',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'telemain12@gmail.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
            else:
                print(password_reset_form.errors)
                password_reset_form.add_error("email", "존재하지 않는 이메일입니다.")
    
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

def social_signup(request):
    messages.error(request, "이미 가입되어 있는 계정입니다.")
    return redirect('todo:todo')

def social_signup_complete(request):
    return render(request, "common/social_signup_complete.html")

# class SocialSignupView(SignupView):
#     form_class = MyCustomSignupForm
#     template_name = "socialaccount/signup.html"

#     def form_invalid(self, form) -> HttpResponse:
#         return super().form_invalid(form)