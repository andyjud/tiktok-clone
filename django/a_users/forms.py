from allauth.account.forms import SignupForm
from django import forms
from django.core.cache import cache
from allauth.account.models import EmailAddress

class CustomSignupForm(SignupForm):
    birthday = forms.DateField()
    code = forms.CharField()
    
    def clean_code(self):
        code = self.cleaned_data.get('code', '').strip()
        email = self.cleaned_data.get('email')
        cached_code = cache.get(f"verification_code_{email}")
        if not cached_code or cached_code != code:
            self.add_error('code', "Invalid or expired verification code.")
    
    def save(self, request):
        user = super().save(request)
        user.birthday = self.cleaned_data.get('birthday')
        user.username = user.username.lower()
        user.email = user.email.lower()
        user.save()
        EmailAddress.objects.filter(user=user, email=user.email).update(verified=True)
        return user
