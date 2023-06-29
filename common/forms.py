from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import forms as auth_forms
# from django.contrib.auth.models import User 
from common.models import User
from allauth.socialaccount.forms import SignupForm
from django.contrib.auth import get_user_model
class LoginForm(forms.Form):
    email = forms.CharField(label = "email", required = False, error_messages={'required' : ''})
    password = forms.CharField(label = "password", required = False)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if not email or not password:
            self.add_error("email", "모든 항목을 입력해주세요.")

class MyCustomSignupForm(SignupForm):
    name = forms.CharField(max_length=10, label = "닉네임")
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "placeholder": "이메일을 입력해주세요.",
                "autocomplete": "email",
            }
        )
    )

    agree_terms = forms.BooleanField(label='서비스 이용약관 및 개인정보방침 동의')
    agree_marketing = forms.BooleanField(label='마케팅 이용 동의')

    def save(self, request):
        print(request)
        user = super(MyCustomSignupForm, self).save(request)
        user.username = self.cleaned_data['name']
        user.agree_terms = self.cleaned_data['agree_terms']
        user.agree_marketing = self.cleaned_data['agree_marketing']
        user.save()
        return user

class UserCreationForm(forms.ModelForm):
    username = forms.CharField(label = "닉네임", required = False)
    password1 = forms.CharField(label = '비밀번호', widget = forms.PasswordInput, required = False)
    password2 = forms.CharField(label = '비밀번호 확인', widget = forms.PasswordInput, required = False)
    email = forms.EmailField(label = '이메일', required = False )
    agree_terms = forms.BooleanField(label = '이용약관', required = False )
    agree_marketing = forms.BooleanField(label = '개인정보처리', required = False)

    class Meta:
        model = User
        fields = ('username', 'email', 'agree_terms', 'agree_marketing')
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        agree_terms = self.cleaned_data.get('agree_terms')
        agree_marketing = self.cleaned_data.get('agree_marketing')

        if username and password1 and password2 and email:
            if not password1.isalnum() or len(password1) < 8 or len(password1) > 20:
                self.add_error("password1", '비밀번호는 8문자 이상 20자 이하의 영어와 숫자를 섞어 설정해주세요.')
                    
            elif password1 != password2:
                self.add_error("password2",'설정하려는 비밀번호와 일치하지 않습니다.' )
            
            if User.objects.filter(email = email):
                self.add_error("email", "이미 존재하는 이메일입니다.")

            if not agree_terms or not agree_marketing:
                self.add_error("agree_terms", "이용약관 및 개인정보처리방침에 동의해주세요.")
                
        else: 
            self.add_error("username", "모든 항목을 채워주세요.")     

    
    def save(self, commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user
