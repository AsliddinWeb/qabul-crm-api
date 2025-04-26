from django.db import models

class DiplomInfo(models.Model):
    DEGREE_LEVEL_CHOICES = [
        ('school', 'Maktab'),
        ('college', 'Kollej'),
        ('university', 'Universitet'),
        ('other', 'Boshqa'),
    ]

    institution_name = models.CharField(max_length=255)
    diplom_number = models.CharField(max_length=50)
    graduation_year = models.PositiveIntegerField()
    degree_level = models.CharField(max_length=50, choices=DEGREE_LEVEL_CHOICES, default='college')
    diplom_file = models.FileField(upload_to='applications/diploms/', null=True, blank=True)

    def __str__(self):
        return f"{self.institution_name} ({self.get_degree_level_display()})"