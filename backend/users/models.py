from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from users.validators import PhoneNumberValidator

from backend.settings.base import AUTH_USER_MODEL

class UserManager(UserManager):

    def _create_user(self, username, email, phone_number, password, **extra_fields):
        """
        Create and save a user with the given 
        username, email, phone_number and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        if not phone_number:
            raise ValueError('The given phone number must be set')
        user = self.model(
            username=username,
            email=email,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, phone_number, password, **extra_fields)

    def create_superuser(self, username, email, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, phone_number, password, **extra_fields)


class User(AbstractUser):

    phone_number_validator = PhoneNumberValidator()

    phone_number = models.CharField(
        _('phone number'),
        max_length=10,
        unique=True,
        validators=[phone_number_validator],
        error_messages={
            'unique': _("A user with that phone number already exists."),
        },
    )

    objects = UserManager()

    REQUIRED_FIELDS = ['email', 'phone_number', ]

    def __str__(self):
        return self.username

        
class UserProfile(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL,related_name='profile',primary_key=True,on_delete=models.CASCADE)
    postcount = models.IntegerField(default=0)
    followercount = models.IntegerField(default=0)
    followingcount = models.IntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)


class Follow(models.Model):

    # Here our user follows the followsuser object
    # for example:
    # A followed B on mann but B did not
    # This Table should have a entry for user=A, followsuser=B
    # But not for the other way around
    # to get all the users that A follows 
    # we can do A.get_following()
    # to get all the users that follows A
    # we can do A.get_followers()

    user = models.ForeignKey(AUTH_USER_MODEL,related_name='following',on_delete=models.CASCADE)
    followsuser = models.ForeignKey(AUTH_USER_MODEL,related_name='followers',on_delete=models.CASCADE)
    followingstatus = models.BooleanField() #add default value as True and use relaymutation to update
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','followsuser')