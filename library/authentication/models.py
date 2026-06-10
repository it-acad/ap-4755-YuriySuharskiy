from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import validate_email
from django.db import models
from django.utils import timezone

ROLE_CHOICES = (
    (0, 'visitor'),
    (1, 'admin'),
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 1)
        extra_fields.setdefault('is_active', True)
        
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    middle_name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    objects = CustomUserManager()

    @property
    def is_staff(self):
        return self.role == 1

    @property
    def is_superuser(self):
        return self.role == 1

    def has_perm(self, perm, obj=None):
        return self.role == 1  # Дозволяємо адміну робити все

    def has_module_perms(self, app_label):
        return self.role == 1  # Дозволяємо адміну бачити всі додатки

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"'id': {self.id}, 'first_name': '{self.first_name}', "
            f"'middle_name': '{self.middle_name}', 'last_name': '{self.last_name}', "
            f"'email': '{self.email}', 'created_at': {self.created_at}, "
            f"'updated_at': {self.updated_at}, 'role': {self.role}, 'is_active': {self.is_active}"
        )

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'

    @staticmethod
    def get_by_id(user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def get_by_email(email):
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
            return True
        except CustomUser.DoesNotExist:
            return False

    @staticmethod
    def create(email, password, first_name=None, middle_name=None, last_name=None):
        if any(len(value or '') > 20 for value in (first_name, middle_name, last_name)):
            return None
        try:
            validate_email(email)
        except Exception:
            return None
        if CustomUser.objects.filter(email=email).exists():
            return None

        now = int(timezone.now().timestamp())
        user = CustomUser(
            email=email,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            created_at=now,
            updated_at=now,
        )
        user.set_password(password)
        user.save()
        return user

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'role': self.role,
            'is_active': self.is_active
        }

    def update(self, first_name=None, last_name=None, middle_name=None, password=None, role=None, is_active=None):
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if middle_name is not None:
            self.middle_name = middle_name
        if password is not None:
            self.password = password
        if role is not None:
            self.role = role
        if is_active is not None:
            self.is_active = is_active

        self.updated_at = int(timezone.now().timestamp())
        self.save()

    @staticmethod
    def get_all():
        return CustomUser.objects.all()

    def get_role_name(self):
        return dict(ROLE_CHOICES).get(self.role, '')