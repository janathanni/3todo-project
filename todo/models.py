from django.db import models
from common.models import User 

class Todo(models.Model):
    #SQLite는 VARCHAR Field에서의 길이를 신경안써서 max_length 값을 줘도 안 통한다.. 그래서 full_clean 메소드를 사용
    todo = models.CharField(max_length = 20)
    user = models.ForeignKey(User, db_column='user', on_delete = models.CASCADE, related_name='user')
    is_done = models.BooleanField(auto_created=False)
    create_date = models.DateTimeField()

    def __str__(self):
        return self.todo

class DoneDays(models.Model):
    user = models.ForeignKey(User, db_column='user', on_delete = models.CASCADE)
    day = models.DateTimeField()

    def __str__(self):
        return str(self.day)