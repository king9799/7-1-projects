from django.db import models
from django.contrib.auth.models import User

# Create your models here.
Choice = (
    ('one', 'start'),
    ('two', 'doing'),
    ('three', 'finish'),
    ('four', 'history')
)


class Todo(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    step = models.CharField(max_length=64, choices=Choice, default='one')
    cr_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class QRcode(models.Model):
    address = models.CharField(max_length=2048, null=True, blank=True)

    def __str__(self):
        self.address = self.address
        return self.address


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images')

    def __str__(self):
        return self.user