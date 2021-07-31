from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, phone, username, password=None):
        if not phone:
            raise ValueError('user must have phone')
        if not username:
            raise ValueError('user must have username')

        user = self.model(phone=phone, username=username, password=password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        if not username:
            raise ValueError('superuser must have username')

        user = self.model(username=username)
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_set_password = True
        user.is_verified = True
        user.save(using=self._db)
        return user
