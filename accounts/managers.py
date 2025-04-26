from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, role='applicant', **extra_fields):
        if not phone:
            raise ValueError("Telefon raqam kiritilishi shart.")
        user = self.model(phone=phone, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone, password, role='admin', **extra_fields)
