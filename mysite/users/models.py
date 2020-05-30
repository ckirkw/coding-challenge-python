from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    def natural_key(self):
        key = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username
        }
        return key
