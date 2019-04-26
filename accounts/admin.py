from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AdminPasswordChangeForm
from django.conf.urls import url

from .models import User, Clients, Company

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super.save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(help_text="Change password here <a href='../password'>Change</a>")

    class Meta:
        model = User
        fields = ('email','password', 'first_name', 'last_name')

        def clean_password(self):

            return self.initial["password"]

class MyAdminPasswordChangeForm(AdminPasswordChangeForm):

    def save(self, commit=True):
        """
        Saves the new password.
        """
        password = self.cleaned_data["password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

class UserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = MyAdminPasswordChangeForm

    list_display = ('email','first_name', 'last_name', 'admin', 'client')

    list_filter = ( 'admin','staff', 'client' )
    
    fieldsets = (
        (None, {
            'fields': (
                'email', 'password'
            ),
        }),
        ('Personal Info', {
                'fields': (
                    'first_name','last_name',
                )
        }),
        ('Permissions', {
                'fields': (
                    'admin','staff', 'client',
                )
        })
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    def get_urls(self):
        return [
               url(
                   r'^(.+)/password/$',
                   self.admin_site.admin_view(self.user_change_password),
                   name='auth_user_password_change',
               ),
           ] + super(UserAdmin, self).get_urls()


admin.site.register(User,UserAdmin)
admin.site.unregister(Group)
admin.site.register(Clients)
admin.site.register(Company)