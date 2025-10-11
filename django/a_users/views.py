from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Count
from django.core.validators import validate_email
import random
import threading
from django.core.cache import cache
from django.core.mail import EmailMessage
from allauth.account.models import EmailAddress
from .forms import ProfileForm, EmailForm, BirthdayForm 

User = get_user_model()


def index_view(request):
    if request.user.is_authenticated:
        return redirect('home') 
    return render(request, 'a_users/index.html')


@login_required
def profile_view(request, username=None):
    if not username:
        return redirect('profile', request.user.username)
    
    if request.GET.get('link'):
        urlpath = reverse('profile', kwargs={'username': username})
        return render(request, 'a_users/partials/_profile_link.html', {"urlpath": urlpath}) 
    
    profile_user = get_object_or_404(User, username=username)
    
    sort_order = request.GET.get('sort', '') 
    if sort_order == 'oldest':
        profile_posts = profile_user.posts.order_by('created_at')
    elif sort_order == 'popular':
        profile_posts = profile_user.posts.annotate(num_likes=Count('likes')).order_by('-num_likes', '-created_at')
    else:
        profile_posts = profile_user.posts.order_by('-created_at')
        
    profile_posts_liked = profile_user.likedposts.all().order_by('-likedpost__created_at')
    profile_user_likes = profile_user.posts.aggregate(total_likes=Count('likes'))['total_likes']
    
    context = {
        'page': 'Profile',
        'profile_user': profile_user,
        'profile_user_likes': profile_user_likes,
        'profile_posts': profile_posts,
        'profile_posts_liked': profile_posts_liked,
    }
    
    if request.GET.get('liked'):
        return render(request, 'a_users/partials/_profile_posts_liked.html', context)  
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


@login_required 
def settings_view(request):
    form = EmailForm(instance=request.user)
    
    if request.GET.get('email'):
        return render(request, 'a_users/partials/_settings_email.html', {'form':form})
    
    if request.POST.get("email"):
        form = EmailForm(request.POST, instance=request.user)
        current_email = request.user.email 
        
        if form.is_valid():
            new_email = form.cleaned_data['email']
            if new_email != current_email:
                form.save()
                email_obj = EmailAddress.objects.get(user=request.user, primary=True)
                email_obj.email = new_email
                email_obj.verified = False
                email_obj.save()
                return redirect('settings')
            
    if request.GET.get('verification'):
        return render(request, 'a_users/partials/_settings_verification.html')
    
    if request.POST.get("code"):
        code = request.POST.get('code').strip()
        email = request.user.email
        cached_code = cache.get(f"verification_code_{email}")
        if cached_code and cached_code == code:
            email_obj = EmailAddress.objects.get(user=request.user, primary=True)
            email_obj.verified = True
            email_obj.save()
            return redirect('settings')
        
    if request.GET.get('birthday'):
        birthdayform = BirthdayForm(instance=request.user)
        return render(request, 'a_users/partials/_settings_birthday.html', {'form':birthdayform})
    
    if request.POST.get("birthday"):
        birthdayform = BirthdayForm(request.POST, instance=request.user)
        if birthdayform.is_valid():
            birthdayform.save()
            return redirect('settings')
        
    if request.POST.get("notifications"):
        if request.POST.get("notifications")  == 'on':
            request.user.notifications = True
        else:
            request.user.notifications = False
        request.user.save()
        return HttpResponse('') 
    
    if request.GET.get("darkmode"):
        if request.GET.get("darkmode") == 'true':
            request.user.darkmode = True
        else:
            request.user.darkmode = False
        request.user.save()
        return HttpResponse('') 
    
    if request.htmx:
        return render(request, "a_users/partials/_settings.html", {'form':form})
    return render(request, "a_users/settings.html", {'form':form})


@login_required
def delete_account(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        return redirect('index')
    
    return render(request, 'a_users/profile_delete.html')
