from django.db import models

class Branch(models.Model):
    """Universitet filiallari (Toshkent, Qarshi va h.k.)"""
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

class EducationForm(models.Model):
    """Ta’lim shakli (masalan: Kunduzgi, Sirtqi)"""
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Degree(models.Model):
    """Ta’lim darajasi (masalan: Bakalavriat, Magistratura)"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Program(models.Model):
    """Yo‘nalishlar (Filialga bevosita bog‘langan)"""
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='programs/program/')
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='programs')
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    duration_years = models.PositiveIntegerField(default=4)

    def __str__(self):
        return f"{self.title} ({self.degree.name} - {self.branch.name})"

class TuitionFee(models.Model):
    """Yo‘nalish + Ta’lim shakli + Filial uchun yillik kontrakt summasi"""
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='tuition_fees')
    education_form = models.ForeignKey(EducationForm, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='UZS')

    class Meta:
        unique_together = ('program', 'education_form', 'branch')

    def __str__(self):
        return f"{self.program.title} - {self.education_form.name} ({self.branch.name}): {self.amount} {self.currency}"
