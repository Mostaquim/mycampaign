from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import transaction, IntegrityError


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
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

    def create_staffuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password
        )
        user.staff = True
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_staffuser(
            email,
            first_name,
            last_name,
            password=password
        )
        user.admin = True
        user.save()
        return user

    def create_clientuser(self, email, first_name, last_name, password):
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
    email = models.EmailField(
        max_length=255, unique=True, verbose_name='email address')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    client = models.BooleanField(default=False)
    accountant = models.BooleanField(default=False)
    objects = MyUserManager()
    user_pic = models.ImageField(null=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.first_name + " " + self.last_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
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

    @property
    def is_accountant(self):
        return self.is_accountant


class ClientManager(models.Manager):
    def create_client(self, email, first_name, last_name, company_name):
        try:
            with transaction.atomic():
                if not email:
                    raise ValueError("An email must be provided")
                user = User.objects.create_clientuser(
                    email, first_name, last_name, None)
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

    def get_or_create_client(
        self,
        company_name,
        full_name,
        phone,
        email,
        street,
        city,
        postcode
    ):
        try:
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                return user.clients
            else:
                names = full_name.split()
                first_name = names[0]
                last_name = names[0]
                if len(names) > 1:
                    last_name = names[1]

                client = Clients.objects.create_client(
                    email, first_name, last_name, company_name)
                client.phone = phone
                client.save()
                client.company.street = street
                client.company.city = city
                client.company.postcode = postcode
                client.company.save()

                return client
        except:
            pass


class Company(models.Model):
    company_name = models.CharField(max_length=255)
    primary_user = models.OneToOneField(
        'clients',
        on_delete=models.SET_NULL,
        null=True,
        related_name='primary_user'
    )
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=50, null=True)
    postcode = models.CharField(max_length=50, null=True)
    vat = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    note = models.TextField(blank=True, null=True)
    terms = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.company_name


class Clients(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        related_name='clients'
    )
    phone = models.CharField(max_length=50, null=True)
    mobile = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=50, null=True)
    postcode = models.CharField(max_length=50, null=True)
    objects = ClientManager()
