# coding: utf-8

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail

class CustomUserManager(BaseUserManager):
    """
    기본 제공 유저를 재정의하여 유저 생성에 필요한 메쏘드 재정의
    """
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError(u'잘못된 이메일')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, True, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    User의 ID를 name이 아닌 email로 사용하기 위해 새로운 User 구현 
    """
    email = models.EmailField(_('email address'), unique=True, max_length=255)
    name = models.CharField(_('name'), max_length=30, blank=True)
#    ip = models.IPAddressField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    
    objects = CustomUserManager() # Default Manager 변경 

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolue_url(self):
        return "/users%/%s/" % urlquote(self.email)

    def get_short_name(self):
        return self.name
    
    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def __str__(self):
        return self.email

class Document(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to='media', blank=True)
 
    def __str__(self):
        return self.title

class Comment(models.Model):
    document = models.ForeignKey(Document)
    content = models.TextField(max_length=2000, null=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document.title +" Comment #"+ str(self.id)

