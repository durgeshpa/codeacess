from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,PermissionsMixin)
from django.core import validators
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.core.mail import send_mail



# Create your models here.

class UserManager(BaseUserManager):
    """class user manager .."""

    def _create_user(self, email_or_phone, password, is_staff, is_superuser, **extra_fields):
        """Create EmailPhoneUser with the given email or phone and password.

        :param str email_or_phone: user email or phone
        :param str password: user password
        :param bool is_staff: whether user staff or not
        :param bool is_superuser: whether user admin or not
        :return settings.AUTH_USER_MODEL user: user
        :raise ValueError: email or phone is not set
        :raise NumberParseException: phone does not have correct format...
        """
        if not email_or_phone:
            raise ValueError('The given email_or_phone must be set')

        if "@" in email_or_phone:
            username, email, phone = (email_or_phone, email_or_phone, "")
        else:
            username, email, phone = (email_or_phone, "", email_or_phone)

        now = timezone.now()
        extra_fields.setdefault('is_staff', True)
        is_active = extra_fields.pop("is_active", True)
        user = self.model(username=username, email=email,
                          mobile=phone,
                          is_staff=is_staff,
                          is_active=is_active,
                          is_superuser=is_superuser,

                          date_joined=now,
                          **extra_fields
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email_or_phone, password=None, **extra_fields):
        """Createing user function .."""
        return self._create_user(email_or_phone, password, False, False, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        """Create and save a SuperUser with the given email and password.."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """docstring for ClassName .."""

    username = models.CharField(max_length=255, unique=True, db_index=True, )

    email = models.EmailField(blank=True, null=True)

    mobile = models.CharField(validators=[validators.RegexValidator(r'^[\+0-9]$',)], max_length=13, blank=True, null=True)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )

    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['password']
    objects = UserManager()

    class Meta:
        """meta class .."""

        permissions = (('can upload problem', 'can upload problem'),)

    def get_full_name(self):
        """Return the full name for the user."""
        return self.username

    def get_short_name(self):
        """Return the short name for the user."""
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
