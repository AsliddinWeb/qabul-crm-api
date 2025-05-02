from django.db import models
from django.conf import settings

class Region(models.Model):
    """Viloyat yoki shaharlar (masalan: Toshkent, Andijon, Qoraqalpog‘iston)"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class District(models.Model):
    """Tumanlar yoki shaharchalar, viloyatga bog‘langan"""
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')

    class Meta:
        unique_together = ('name', 'region')

    def __str__(self):
        return f"{self.name}, {self.region.name}"

class PassportInfo(models.Model):
    """Pasport ma’lumotlari (viloyat va tuman tanlanadi)"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    passport_series = models.CharField(max_length=50)
    passport_number = models.CharField(max_length=50)
    given_by = models.CharField(max_length=255)
    address = models.TextField()
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='applications/passport/', null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.passport_series}{self.passport_number})"
