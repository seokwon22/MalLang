from django.db import models


class Board(models.Model):
    user_id = models.CharField(max_length=30)
    nickname = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    image = models.ImageField(null=True, blank=True)
    date = models.DateTimeField()
    def __str__(self):
        return str({"user_id": self.user_id,
                    "nickname": self.nickname,
                    "title": self.title,
                    "content": self.content,
                    "image": self.image,
                    "date": self.date})



class Member(models.Model):
    nickname = models.CharField(max_length=20)
    user_id = models.CharField(primary_key=True, max_length=30)
    password = models.CharField(max_length=300)

    def __str__(self):
        return str({"nickname": self.nickname,
                    "user_id": self.user_id,
                    "password": self.password
                    })


class Diary(models.Model):
    user_id = models.CharField(max_length=20)
    diarydate = models.DateTimeField()
    diaryweather = models.CharField(max_length=50)
    diaryemoji = models.CharField(max_length=100)
    diarycontent = models.TextField()
    image= models.ImageField(upload_to='diaryimages/' ,null=True, blank=True)  # 이미지 필드 추가
    

    def __str__(self):
        return str({"user_id": self.user_id,
                    "diarydate": self.diarydate,
                    "diaryweather": self.diaryweather,
                    "diaryemoji": self.diaryemoji,
                    "diarycontent": self.diarycontent,
                    "image":self.image,
                    })