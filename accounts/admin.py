from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PhoneVerification

# Unfold
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    
    model = User
    list_display = ('phone', 'full_name', 'role', 'is_verified', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_verified', 'is_staff')
    search_fields = ('phone', 'full_name')
    ordering = ('-id',)

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Shaxsiy maʼlumotlar', {'fields': ('full_name',)}),
        ('Rol va ruxsatlar', {
            'fields': ('role', 'is_verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Muhim sanalar', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'full_name', 'role', 'is_verified', 'is_active', 'is_staff')}
         ),
    )

    filter_horizontal = ('groups', 'user_permissions')


@admin.register(PhoneVerification)
class PhoneVerificationAdmin(ModelAdmin):
    list_display = ('phone', 'code', 'created_at', 'is_expired_status')
    search_fields = ('phone',)
    list_filter = ('created_at',)

    def is_expired_status(self, obj):
        return obj.is_expired()
    is_expired_status.boolean = True
    is_expired_status.short_description = 'Muddati tugaganmi?'
