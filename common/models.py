from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, agree_terms, agree_marketing, username, password = None):
        if not username:
            raise ValueError('Users must have an username.')

        if not email:
            raise ValueError('Users must have an email address.')
        
        user = self.model(
            username = username,
            email = self.normalize_email(email),
            agree_terms = agree_terms,
            agree_marketing = agree_marketing
        )

        user.set_password(password)
        user.save(using = self._db)

        return user 

    def create_superuser(self, username, email, password) :
        user = self.create_user(
            username = username,
            email = self.normalize_email(email),
            password = password,
            agree_terms = True,
            agree_marketing = True
        )

        user.is_admin = True 
        user.save(using = self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length = 10)
    email = models.EmailField(max_length = 255, 
                            unique = True, 
                            error_messages={'unique' : "이미 존재하는 이메일입니다.",
                                            'required' : ""}, primary_key=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    agree_terms = models.BooleanField(default=False)
    agree_marketing = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['agree_terms', 'agree_marketing']
    class Meta:
        db_table ='user'

    def get_full_name(self):
        pass 

    def get_short_name(self):
        pass

    @property 
    def is_superuser(self):
        return self.is_admin 
    
    def has_perm(self, perm, obj = None):
        return self.is_admin 

    def has_module_perms(self, app_label):
        return self.is_admin 

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.email

    objects = UserManager()

    USERNAME_FIELD = 'email'