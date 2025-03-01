from django.core.exceptions import ValidationError
from django.db import models
from myproject.common.models import BaseModel
from myproject.users.models import BaseUser
# Create your models here.


class Post(BaseModel):
    slug = models.SlugField(primary_key=True, max_length=200)
    author = models.ForeignKey(BaseUser, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.slug


class Subscribtion(BaseModel):
    subscriber = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='subs')
    target = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='targets')

    class Meta:
        uinque_toghether = ('subscriber', 'target')

    def clean(self):
        if self.subscriber == self.target:
            raise ValidationError({"subscriber": ("subscriber can not be equal to targer")})

    def __str__(self):
        return f"{self.subscriber.email} subscribe {self.target.email}"
