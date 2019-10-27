#python imports
# import uuid

#django/rest_framework imports
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

#project level imports
from libs.models import TimeStampedModel

#third paty imports
from model_utils import Choices


class User(TimeStampedModel):

    mobile = models.BigIntegerField(unique=True,
        validators=[
            MinValueValidator(5000000000),
            MaxValueValidator(9999999999),
        ]
    )
    GENDER = Choices(
        ('M','Male'),
        ('F','Female'),
        ('O','Other')
    )
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    first_name = models.CharField(max_length=5, blank=False)
    last_name = models.CharField(max_length=64, blank=False)
    email = models.EmailField(max_length=128, unique=True, db_index=True, blank=False)
    password = models.CharField(max_length=20)
    gender = models.CharField(choices=GENDER, max_length=1, blank=False)
    address = models.TextField(blank=False,default='')
    is_admin = models.BooleanField(default=False)

    class Meta:
        app_label = 'account'
        db_table = 'api_user'

    @property
    def full_name(self):
        return "{fn} {ln}".format(fn=self.first_name, ln=self.last_name)

    # @property
    # def access_token(self):
    #     token, is_created = Token.objects.get_or_create(user=self)
    #     return token.key