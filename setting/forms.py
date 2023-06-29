from django import forms

class DeleteUserForm(forms.Form):
    origin_password = forms.CharField(max_length = 20,
                                        label = "현재 비밀번호",
                                        error_messages={'required' : '비밀번호를 입력해주세요.'}
                                        )

class SetPassword(forms.Form):
    origin_password = forms.CharField(max_length = 20,
                                        label = "현재 비밀번호",
                                        error_messages={'required' : ''}
                                        )
    new_password = forms.CharField(max_length = 20,
                                        label = "새 비밀번호",
                                        error_messages={'required' : ''}
                                        )
    confirm_password = forms.CharField(max_length = 20,
                                        label = "새 비밀번호 확인",
                                        error_messages={'required' : ''}
                                        )
        
    def clean(self):
        cleaned_data = super().clean()
        origin_password = cleaned_data.get('origin_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if origin_password and new_password and confirm_password:

            if origin_password == new_password:
                self.add_error('new_password', '이전과 같은 비밀번호를 사용할 수 없습니다.')
                print("niniz")
                
            else:
                if len(new_password) < 8 or not new_password.isalnum():
                    self.add_error('new_password', '비밀번호는 8~20자 영문 대 소문자, 숫자를 사용해주세요.')

                elif new_password != confirm_password:
                    self.add_error('confirm_password', '설정하려는 비밀번호와 일치하지 않습니다.')
        else:
            self.add_error('origin_password', "모든 칸을 채워주세요.")