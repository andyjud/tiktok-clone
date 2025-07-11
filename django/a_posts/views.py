from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post

def home_view(request):
    posts = Post.objects.order_by('-created_at')
    context = {
        'page': 'Home',
        'posts': posts,
    }
    if request.htmx:
        return render(request, 'a_posts/partials/_home.html', context)
    return render(request, 'a_posts/home.html', context)


def explore_view(request):
    posts = Post.objects.order_by('-created_at')
    context = {
        'page': 'Explore',
        'posts': posts,
    }
    if request.htmx:
        return render(request, 'a_posts/partials/_explore.html', context)
    return render(request, 'a_posts/explore.html', context)


def upload_view(request):
    form = PostForm()
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    
    context = {
        'page': 'Upload',
        'form': form,
    }
    if request.htmx:
        return render(request, 'a_posts/partials/_upload.html', context)
    return render(request, 'a_posts/upload.html', context)
