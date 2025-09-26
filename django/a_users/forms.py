from allauth.account.forms import SignupForm
from django import forms
from django.core.cache import cache
from allauth.account.models import EmailAddress
from .models import CustomUser

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
    
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['image', 'username', 'name', 'bio', 'website']
        widgets = {
            'username' : forms.TextInput(attrs={'class': 'input-field','placeholder': 'Username'}),
            'name' : forms.TextInput(attrs={'class': 'input-field','placeholder': 'Name'}),
            'bio' : forms.Textarea(attrs={'class': 'input-field resize-none','rows':2, 'placeholder': 'Bio', 'maxlength': '250'}),
            'website' : forms.TextInput(attrs={'class': 'input-field','placeholder': 'Website'}),
        }
        
        
class EmailForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']
        widgets = {
            'email' : forms.TextInput(attrs={'class': 'input-field w-full', 'placeholder': 'Email'}),
        }
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.exclude(id=self.instance.id).filter(email=email).exists():
            raise forms.ValidationError("This email is already taken.")
        return email
    

class BirthdayForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['birthday']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'input-field w-full'}),
        }
