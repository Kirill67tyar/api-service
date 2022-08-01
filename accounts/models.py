from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, identify_hasher, check_password
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
        Creates and saves a User with the given email, and password.
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
        Creates and saves a superuser with the given email,  and password.
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

    def __repr__(self):
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

    def get_short_name(self):
        if not self.name:
            return self.email
        return self.name

    def save(self, *args, **kwargs):
        """
        когда мы создаём superuser через консоль, то
        Django хеширует  этот пароль, и он прилетает сюда
        уже захешированным.
        Когда же мы сохраняем экземпляр User через код в обработчиках,
        то мы имеем дело с обычным текстом.
        Поэтому, если пароль захеширован, то его нужно просто сохранить,
        чтобы он ещё не захэшировался.
        А если не хэшированный, то захэшировать и сохранить
        В админке мы переопределили UserCreationForm, которая хэширует пароль
        """
        try:
            identify_hasher(self.password)
        except ValueError:
            self.password = make_password(password=self.password)
        super().save(*args, **kwargs)
