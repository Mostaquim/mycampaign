from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import transaction,IntegrityError

class MyUserManager(BaseUserManager):
    def create_user(self,email,first_name, last_name,password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        
        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self,email,first_name, last_name,password):
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password
        )
        user.staff = True
        user.save()
        return user

    def create_superuser(self,email,first_name, last_name,password):
        user = self.create_staffuser(
            email,
            first_name,
            last_name,
            password=password
        )
        user.admin = True
        user.save()
        return user

    def create_clientuser(self,email,first_name, last_name,password):
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password
        )
        user.client = True
        user.save()
        return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, verbose_name='email address')
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    client = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD='email'

    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return self.email

    def has_perm(self,perm, obj=None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def get_fullname(self):
        return self.first_name 

    @property
    def is_staff(self):
        return self.staff

    @property 
    def is_superuser(self):
        return self.admin

    @property
    def is_client(self):
        return self.client

    @property
    def is_active(self):
        return self.active

class ClientManager(models.Manager):
    def create_client(self, email, first_name, last_name, company_name):
        try:
            with transaction.atomic():
                if not email:
                    raise ValueError("An email must be provided")
                user = User.objects.create_clientuser(email, first_name, last_name, None)
                company = Company(company_name=company_name)
                company.save()
                client = self.model(
                    user=user,
                    company=company
                )
                client.save()
                company.primary_user = client
                company.save()
                return client
        except IntegrityError as error:
            print(repr(error))

class Company(models.Model):
    company_name = models.CharField(max_length=255)
    primary_user = models.ForeignKey('clients', related_name="primary_client", on_delete=models.SET_NULL, null=True, blank=True)

class Clients(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.OneToOneField(Company,on_delete=models.SET_NULL,null=True)
    objects = ClientManager()
