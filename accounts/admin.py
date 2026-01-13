from django.contrib import admin
from accounts.models import  VerificationCode, User
# Register your models here.
admin.site.register(VerificationCode)
from accounts.forms import UserAdminCreationForm, UserAdminChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin, admin.ModelAdmin,):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = (
        "first_name",
        "last_name",
        "email",
        "user_type",
        "is_active",
        "phone_number"
       
    )
    list_filter = (
        "user_type",
        "is_active",

    )
    fieldsets = (
        (None, {"fields": (
            "email",
            "password",
       
        )}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "user_type",
                 
                )
            },
        ),
        (
        "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    'groups', 
                    'user_permissions',

                )
            },
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": (
            "email",
            "first_name",
            "last_name",
            "user_type",
            "phone_number",
            "password"
         
        )}),
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
    )

    ordering = ("first_name","last_name")
    filter_horizontal = ()
    actions = [
        "disable_users",
        "enable_users",
    ]
    
    def save_model(self, request, obj, form, change):
        return super().save_model(request, obj, form, change)


    def disable_users(self, request, queryset):
        queryset.update(is_active=False)

    def enable_users(self, request, queryset):
        queryset.update(is_active=True)



    def has_add_permission(self, request) -> bool:
        if request.user.is_staff :
            return True
        return False

admin.site.register(User, UserAdmin)