from django.db import models
from django.conf import settings
from programs.models import TuitionFee
from .passport import PassportInfo
from .diplom import DiplomInfo

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Yuborilgan'),
        ('review', 'Ko‘rib chiqilmoqda'),
        ('accepted', 'Qabul qilindi'),
        ('rejected', 'Rad etildi'),
    ]

    ADMISSION_TYPE_CHOICES = [
        ('regular', '1-kurs (yangi qabul)'),
        ('transfer', 'Perevod (o‘qishni ko‘chirish)'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    passport = models.OneToOneField(PassportInfo, on_delete=models.CASCADE, related_name='application')
    diplom = models.ForeignKey(DiplomInfo, on_delete=models.CASCADE, related_name='applications')
    tuition_fee = models.ForeignKey(TuitionFee, on_delete=models.SET_NULL, null=True)
    admission_type = models.CharField(max_length=20, choices=ADMISSION_TYPE_CHOICES, default='regular')
    study_year = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.passport.full_name} - {self.tuition_fee.program.title} ({self.get_admission_type_display()})"

# class UploadedDocument(models.Model):
#     application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
#     file = models.FileField(upload_to='applications/documents/')
#     doc_type = models.CharField(max_length=50, help_text="Masalan: pasport, diplom, rasm")

#     def __str__(self):
#         return f"{self.doc_type} - {self.application.passport.full_name}"