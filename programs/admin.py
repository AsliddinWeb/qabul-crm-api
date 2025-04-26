from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.admin import BaseModelAdmin, StackedInline
from django.utils.html import format_html
from .models import Branch, EducationForm, Degree, Program, TuitionFee

@admin.register(Branch)
class BranchAdmin(ModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name', 'address')
    fieldsets = (
        ("Filial ma'lumotlari", {
            "fields": ('name', 'address', 'phone', 'email')
        }),
    )

@admin.register(EducationForm)
class EducationFormAdmin(ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')
    fieldsets = (
        ("Ta'lim shakli", {
            "fields": ('code', 'name')
        }),
    )

@admin.register(Degree)
class DegreeAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fieldsets = (
        ("Ta'lim darajasi", {
            "fields": ('name',)
        }),
    )

class TuitionFeeInline(StackedInline):
    model = TuitionFee
    extra = 0
    fields = ('education_form', 'branch', 'amount', 'currency')
    show_change_link = True

@admin.register(Program)
class ProgramAdmin(ModelAdmin):
    list_display = ('title', 'code', 'degree', 'branch', 'duration_years', 'preview_image')
    list_filter = ('degree', 'branch')
    search_fields = ('title', 'code', 'description')
    inlines = [TuitionFeeInline]
    readonly_fields = ('preview_image',)

    tabs = [
        ("Asosiy ma'lumotlar", {
            "fields": ('title', 'code', 'degree', 'branch', 'duration_years'),
        }),
        ("Tavsif va rasm", {
            "fields": ('image', 'preview_image', 'description'),
        }),
    ]

    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 120px; object-fit: cover;" />',
                obj.image.url
            )
        return "No image"
    preview_image.short_description = "Rasm ko‘rinishi"

@admin.register(TuitionFee)
class TuitionFeeAdmin(ModelAdmin):
    list_display = ('program', 'education_form', 'branch', 'amount', 'currency')
    list_filter = ('education_form', 'branch')
    search_fields = ('program__title',)
    fieldsets = (
        ("To‘lov haqida", {
            "fields": ('program', 'education_form', 'branch', 'amount', 'currency'),
        }),
    )
