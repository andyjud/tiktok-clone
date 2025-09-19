from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.validators import validate_email
import random
import threading
from django.core.cache import cache
from django.core.mail import EmailMessage
from .forms import ProfileForm

User = get_user_model()


def index_view(request):
    return render(request, 'a_users/index.html')


@login_required
def profile_view(request, username=None):
    if not username:
        return redirect('profile', request.user.username)
    
    profile_user = get_object_or_404(User, username=username)
    
    sort_order = request.GET.get('sort', '') 
    if sort_order == 'oldest':
        profile_posts = profile_user.posts.order_by('created_at')
    else:
        profile_posts = profile_user.posts.order_by('-created_at')
    
    context = {
        'page': 'Profile',
        'profile_user': profile_user,
        'profile_posts': profile_posts,
    }
    
    if request.GET.get('sort'):
        return render(request, 'a_users/partials/_profile_posts.html', context)  
    if request.htmx:
        return render(request, 'a_users/partials/_profile.html', context)
    return render(request, 'a_users/profile.html', context)


def verification_code(request):
    email = request.GET.get("email")
    if not email:
        return HttpResponse('<p class="error">Email is required.</p>')
    
    try:
        validate_email(email)
    except:
        return HttpResponse('<p class="error">Invalid email address provided.</p>')
    
    code = str(random.randint(100000, 999999))
    cache.set(f"verification_code_{email}", code, timeout=300)
    subject = "Your TikTok Verification Code"
    message = f"Use this code to sign up: {code}. It expires in 5 minutes."
    sender = "no-reply@tiktok-clone.com"
    recipients = [email]
    
    email_thread = threading.Thread(target=send_email_async, args=(subject, message, sender, recipients))
    email_thread.start()
       
    return HttpResponse('<p class="success">Verification code sent to your email!</p>')


def send_email_async(subject, message, sender, recipients):
    email = EmailMessage(subject, message, sender, recipients)
    email.send()
    
    
@login_required    
def profile_edit(request):
    form = ProfileForm(instance=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.username)
    
    if request.htmx:
        return render(request, "a_users/partials/_profile_edit.html", {'form' : form})
    return redirect('profile', request.user.username) 
