from django.db import models


class Entry(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    linkedin= models.URLField(max_length=200)
    photo = models.ImageField(upload_to='images/')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self) -> str:
        return self.first_name
    