from django.db import models
import os
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, name, phoneNumber,password=None, password2=None):
        """
        Creates and saves a User with the given email, name, phoneNumber and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phoneNumber=phoneNumber,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phoneNumber, password=None):
        """
        Creates and saves a superuser with the given email, name, phoneNumber
         and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            phoneNumber=phoneNumber,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

def get_upload_path(instance, filename):
    return os.path.join('profilePic',str(instance.name),filename)

# Create your  custom models here.
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    phoneNumber= models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)
    profilePic= models.ImageField(upload_to=get_upload_path,
                                  null=True, blank=True)



    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name','phoneNumber']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



# model for setting user profile picture

# class UserProfilePic(models.Model):
#     user= models.OneToOneField(User,on_delete=models.CASCADE)
#     profilePic= models.ImageField(upload_to='',
#                                   null=True, blank=True)
    
#     def __str__(self):
#         return self.user
    
