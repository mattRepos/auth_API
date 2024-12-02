from django.db import models

class User(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    user_inv_code = models.CharField(max_length=6)
    activated_inv_code = models.CharField(max_length=6,null=True, blank=True)

    def __str__(self):
        return self.phone_number