from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
)
from django.db.models import (
    EmailField, BooleanField,
    DateTimeField, CharField
)


class MyUserManager(BaseUserManager):
    # use_in_migrations = True

    def create_user(self, email, password=None, **kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Пользователь Должен предоставить email для регистрации')
        if not password:
            raise ValueError('Пользователь должен ввести пароль')
        user = self.model(
            email=self.normalize_email(email), **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    name = CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='name',
    )
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    is_admin = BooleanField(default=False)
    timestamp = DateTimeField(auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # для дополнительных полей помимо USERNAME_FIELD

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # def save(self, *args, **kwargs):
    #     self.password = make_password(self.password)
    #     return super().save(*args, **kwargs)
