from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from accounts.models import User,  UserOtherEmails, UserContact, UserEmergencyContact, UserPostalAddress, \
    UserResidentialAddress, UserPayments, BaseTimeStamp
from business.models import BusinessGeneralSettings
from locations.models import  Location, location_phone_choices, location_email_choices, LocationPhone, \
    location_web_choices, location_im_choices, location_event_choices, location_address_choices, LocationAddress
from permissions.models import Permissions, PermissionMode, RollPermission, PermissionModule
from positions.models import UserPosition, Positions


admin.autodiscover()

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            print "commmit"
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_("Raw passwords are not stored, so there is no way to see "
                                                     "this user's password, but you can change the password "
                                                     "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions')
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserPostionInline(admin.TabularInline):
    extra = 1
    model = UserPosition


class UserOtherEmailsInline(admin.TabularInline):
    extra = 1
    model = UserOtherEmails


class UserContactInline(admin.TabularInline):
    extra = 1
    model = UserContact


class UserEmergencyContactInline(admin.TabularInline):
    extra = 1
    model = UserEmergencyContact


class UserPostalAddressInline(admin.TabularInline):
    extra = 1
    model = UserPostalAddress


class UserResidentialAddressInline(admin.TabularInline):
    extra = 1
    model = UserResidentialAddress


class UserPaymentsInline(admin.TabularInline):
    extra = 1
    model = UserPayments


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('first_name', 'last_name', 'username', 'email', 'is_superuser')
    list_filter = ('first_name',)
    inlines = [UserPostionInline, UserOtherEmailsInline, UserContactInline, UserEmergencyContactInline,
               UserPostalAddressInline, UserResidentialAddressInline, UserPaymentsInline]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'profile_pic','active_position')}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser'
                                       )}),
        (_('Created By'), {'fields': ('created_by', 'modified_by'
                                      )}),

        (_('Important dates'), {'fields': ('last_login', 'start_date', 'date_of_birth')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()





class PermissionCategoryInline(admin.TabularInline):
    extra = 1
    model = Permissions


class PermissionModeInline(admin.TabularInline):
    extra = 1
    model = PermissionMode


class UserPermssionInline(admin.TabularInline):
    extra = 1
    model = RollPermission

class PermissionAdmin(admin.ModelAdmin):
    inlines = [
        UserPermssionInline
    ]


admin.site.register(User, MyUserAdmin)
admin.site.register(BaseTimeStamp)
admin.site.register(Location)
admin.site.register(Positions, PermissionAdmin)
admin.site.register(PermissionMode)
admin.site.register(UserPosition)
admin.site.register(Permissions)
admin.site.register(PermissionModule)
admin.site.register(BusinessGeneralSettings)
admin.site.register(RollPermission)
admin.site.register(LocationPhone)
admin.site.register(location_web_choices)
admin.site.register(location_im_choices)
admin.site.register(LocationAddress)
admin.site.register(location_event_choices)
admin.site.register(location_address_choices)
admin.site.register(location_phone_choices)
admin.site.register(location_email_choices)

