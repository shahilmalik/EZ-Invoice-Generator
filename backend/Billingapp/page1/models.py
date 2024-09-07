from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _



class Client(models.Model):
    name = models.CharField(max_length=20, blank=False)
    gst = models.CharField(max_length=16, blank=False, null=True, default=None)
    email = models.CharField(max_length=25, blank=True, null=True)
    phone = models.CharField(max_length=15)
    address_line1 = models.CharField(max_length=20, null=True, blank=True)
    address_line2 = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=15, null=True, blank=True)
    pincode = models.CharField(max_length=6,null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)


class Service(models.Model):
    name = models.CharField(max_length=50, blank=False)
    price = models.CharField(max_length=1000, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)


class Profile(models.Model):
    company_name = models.CharField(max_length=20, blank=True)
    company_gst = models.CharField(max_length=16, blank=True)
    company_address_line1 = models.CharField(max_length=20, blank=True)
    company_address_line2= models.CharField(max_length=20, blank=True)
    company_city = models.CharField(max_length=20, blank=True)
    company_state = models.CharField(max_length=15, blank=True)
    company_pincode = models.CharField(max_length=20, blank=True)
    account_name=models.CharField(max_length=20,blank=True,null=True)
    account=models.CharField(max_length=20,blank=True,null=True)
    ifsc=models.CharField(max_length=11,blank=True,null=True)
    phone_number=models.CharField(max_length=10,blank=True,null=True,default='phone')
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.company_name


    def save(self, *args, **kwargs):
        if not self.pk and not self.user_id:  # if the object is being created and user_id is not set
            super().save(*args, **kwargs)  # save the model first to get a valid primary key
            profile = Profile.objects.create(
                company_name='Company Name',
                company_gst="company GST",
                company_address_line1="Line 1..",
                company_address_line2="Line 2..",
                company_city="City",
                company_state="State",
                company_pincode="pin..",
                account_name="Account Name",
                account="Account No.",
                ifsc="IFSC",
                user=self
            )
            self.profile = profile
        super().save(*args, **kwargs)


class CustomUser(AbstractUser):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_profile', null=True, blank=True)

    class Meta:
        # specify the app_label to avoid issues when using Django's default User model
        app_label = 'home'

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

