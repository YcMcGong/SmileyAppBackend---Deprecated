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

    def get_user_id(self):
        return self.user_id

    def get_username(self):
        return self.username

    def get_experience(self):
        return self.experience

    def get_exp_id(self):
        return self.exp_id

    def get_email(self):
        return self.email

    # Edition of user data

    def edit_user_id(self, user_id):
        self.user_id = user_id
        self.save()

    def edit_username(self, username):
        self.username = username
        self.save()

    def edit_experience(self, experience):
        self.experience = experience
        self.save()

    def edit_exp_id(self, exp_id):
        self.exp_id = exp_id
        self.save()

    def edit_email(self, email):
        self.email = email
        self.save()

