from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages, auth
from setting.forms import SetPassword, DeleteUserForm
from allauth.socialaccount.models import SocialAccount


# Create your views here.
@login_required(login_url='common:login')
def setting(request):
    user = request.user
    return render(request, "setting/settings.html", {'username' : user.username})

@login_required(login_url='common:login')
def set_password(request):
    if request.method == 'POST':
        user = request.user
        form = SetPassword(request.POST)

        if form.is_valid():
            #현재 password가 입력한 password와 일치할 때 비밀번호를 변경할 수 있도록 한다. 
            print(form.data['origin_password'], user.password)
            if check_password(form.data['origin_password'], user.password):
                user.set_password(form.data['new_password'])
                user.save()
                messages.success(request, "비밀번호 변경 성공")
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            else:
                form.add_error('origin_password', "현재 비밀번호가 일치하지 않습니다.")
                
                
        return render(request, "setting/set_password.html", {'form' :form})
    
    else:
        form = SetPassword()
        return render(request, 'setting/set_password.html', {'form' : form})

@login_required(login_url='common:login')
def resign(request):
    user = request.user
    if SocialAccount.objects.filter(user=user).exists():
        if request.method == "POST":
            user = request.user
            resign_check = request.POST.get("agree")

            if resign_check:
                request.user.delete()
                SocialAccount.objects.filter(user=user).delete()
                return render(request, 'setting/resign_success.html')
                
            else:
                messages.error(request, "항목에 동의해주세요.")
                return render(request, 'setting/resign.html')

        else:
            return render(request, 'setting/resign.html')

    else:
        if request.method == "POST":
            form = DeleteUserForm(request.POST)
            user = request.user
            origin_password = form.data["origin_password"]
            resign_check = request.POST["agree"]

            if check_password(origin_password, user.password):
                if resign_check:
                    request.user.delete()

                    return render(request, 'setting/resign_success.html')
                
                else:
                    form.add_error("agree", "항목에 동의해주세요.")
                    return render(request, 'setting/resign.html', {'form' :form})   
            
            else:
                form.add_error("origin_password", "비밀번호가 틀렸습니다.")
                return render(request, 'setting/resign.html', {'form' :form})

        else:
            form = DeleteUserForm()
            return render(request, 'setting/resign.html', {'form' :form})

@login_required(login_url='common:login')
def set_username(request):
    if request.method == "POST":
        new_username = request.POST.get("set-nickname").strip()

        if new_username:
            user = request.user
            user.username = new_username
            user.save()
            messages.success(request, "변경 사항을 저장했습니다.")
            return render(request, 'setting/set_username.html')
        
        else:
            messages.error(request, "변경 사항을 입력해주세요.")
            return render(request, 'setting/set_username.html')
    else:
        return render(request, 'setting/set_username.html')

def agreements(request):
    return render(request, 'setting/agreements.html')