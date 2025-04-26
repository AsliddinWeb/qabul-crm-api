from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline, BaseModelAdmin
from .models import (
    Application,
    PassportInfo,
    Region,
    District,
    DiplomInfo,
)

# ✅ Viloyat va Tumanlar
@admin.register(Region)
class RegionAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(District)
class DistrictAdmin(ModelAdmin):
    list_display = ('name', 'region')
    list_filter = ('region',)
    search_fields = ('name',)

# ✅ Diplomlar
@admin.register(DiplomInfo)
class DiplomInfoAdmin(ModelAdmin):
    list_display = ('institution_name', 'diplom_number', 'graduation_year', 'degree_level')
    list_filter = ('degree_level', 'graduation_year')
    search_fields = ('institution_name', 'diplom_number')

# ✅ Pasportlar
@admin.register(PassportInfo)
class PassportInfoAdmin(ModelAdmin):
    list_display = ('full_name', 'passport_series', 'passport_number', 'region', 'district')
    list_filter = ('region', 'district')
    search_fields = ('full_name', 'passport_number', 'passport_series')

# ✅ Hujjatlar (Inline ko‘rinish)
# class UploadedDocumentInline(StackedInline):
#     model = UploadedDocument
#     extra = 0
#     fields = ('doc_type', 'file')
#     show_change_link = True

# ✅ Asosiy Application — unfold Tabbed ko‘rinishda
@admin.register(Application)
class ApplicationAdmin(ModelAdmin):
    list_display = ('passport', 'tuition_fee', 'admission_type', 'study_year', 'status')
    list_filter = ('status', 'admission_type', 'tuition_fee__branch', 'tuition_fee__education_form')
    search_fields = ('passport__full_name', 'passport__passport_number')
    readonly_fields = ('submitted_at',)
    # inlines = [UploadedDocumentInline]

    tabs = [
        ("Asosiy ma’lumotlar", {
            "fields": (
                'user', 'passport', 'diplom', 'tuition_fee',
                'admission_type', 'study_year', 'status', 'submitted_at',
            )
        }),
    ]
