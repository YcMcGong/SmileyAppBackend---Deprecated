from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    
    use_in_migrations = True
  
    """
    create_user will be used when creating a regular user
    """
    def create_user(self, user_id, password, **extras):
        if not user_id:
            raise ValueError('user_id is required')
        # BaseUserManager.normalize_email converts domain to lowercase
        user = self.model(
            user_id=user_id,
            **extras
        )
        # set_password will take take of the hashing
        user.set_password(password)
        user.save()
        return user

    """
    create_superuser will be used when creating a superuser
    """
    def create_superuser(self, user_id, password, **extras):
        if not user_id:
            raise ValueError('user_id is required')
        user = self.model(
            user_id=user_id,
            **extras
        )
        user.set_password(password)
        # make sure the user is staff and a superuser
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


"""
For our custom user model, we should start by inheriting from
the AbstractBaseUser and PermissionsMixin classes
"""
class User(AbstractBaseUser, PermissionsMixin):
    
    user_id = models.CharField('user_id', max_length=150, unique=True,)
    exp_id = models.CharField(max_length=25, blank=True, null=True)
    username = models.CharField( max_length=25, blank=True, null=True)
    experience = models.IntegerField(default=None, blank=True, null=True)
    email = models.EmailField(default=None, blank=True, null=True)

    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField(default=False)

    # specify the Manager for the User
    objects = CustomUserManager()

    # specify the 'username' field of the model, must be unique
    # this is required by AbstractBaseUser
    USERNAME_FIELD = 'user_id'
    # list of fields required when creating a superuser
    REQUIRED_FIELDS = []

    """
    AbstractBaseUser requires get_full_name and get_short_name
    to be implemented by the subclass
    """
    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.get_full_name()

