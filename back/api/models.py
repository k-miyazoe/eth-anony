from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def _create_user(self, user_key, password, **extra_fields):
        if not user_key:
            raise ValueError('userkeyは必須です')

        user = self.model(user_key=user_key, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self, user_key, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(user_key, password, **extra_fields)

    def create_superuser(self, user_key, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(user_key, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    #pkではなく、パスワード認証の際に使うもの 
    #user_keyは被った場合どうなるのか挙動を確認する
    user_key = models.CharField(default="",max_length=255,unique=True)
    user_email = models.EmailField("メールアドレス",default="",max_length=255)
    user_name = models.CharField("名前",default="",max_length=255)
    #変更箇所
    user_wallet = models.IntegerField(default=0)
    user_eth_address = models.CharField(default="",max_length=50)
    user_eth_password = models.CharField(default="",max_length=20)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    #追加カラム
    user_point = models.IntegerField(default=0)
    user_group = models.BooleanField(null=True)
    
    objects = UserManager()

    #USERNAME_FIELDで指定したフィールドは、ログイン認証やメール送信などで利用します。
    # ここをemailにすることでメールアドレスでのログインが可能になります。
    # 指定したフィールドは一意である必要があるため、ここで指定できるフィールドはunique=Trueである必要があります。
    USERNAME_FIELD = 'user_key'
    #ターミナルでユーザー作成（manage.py createsuperuser）するときに表示される項目です。
    # ユーザーは指定した項目の値を入力するよう求められます。
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.user_key

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_user_name = models.CharField(null=True,max_length=255)
    question_title = models.CharField(default="タイトル",max_length=50)
    question_content = models.TextField(default="内容")
    question_source_code = models.TextField(null=True)
    question_post_time = models.DateTimeField(auto_now_add=True)
    question_status = models.BooleanField(default=False)
    question_value = models.IntegerField(default=0)
    question_number_of_responses = models.IntegerField(default=0)
    #閲覧回数[new]
    question_views = models.IntegerField(default=0)
    #bad評価
    question_bad_value = models.IntegerField(default=0)
    #追加
    question_group = models.BooleanField(null=True)
    question_eth_address = models.CharField(default="",max_length=50)
    
    
    class Meta:
        ordering = ['question_post_time']

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question,on_delete=models.CASCADE)
    answer_user_name = models.CharField(null=True,max_length=255)
    answer_content = models.TextField(default="内容")
    answer_source_code = models.TextField(null=True)
    answer_post_time = models.DateTimeField(auto_now_add=True)
    answer_value = models.IntegerField(default=0)
    answer_best = models.BooleanField(default=False)
    #bad評価
    answer_bad_value = models.IntegerField(default=0)
    #追加
    answer_eth_address = models.CharField(default="",max_length=50)

#質問いいね
class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
#回答いいね
class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

#質問bad
class QuestionBad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
#回答bad
class AnswerBad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)