from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from .forms import PostForm, PostEditForm
from .models import Post


@login_required
def home_view(request):
    posts = Post.objects.order_by('-created_at')
    
    paginator = Paginator(posts, 1)
    page_number = int(request.GET.get('page_number', 1))
    posts_page = paginator.get_page(page_number) 
    next_page = posts_page.next_page_number() if posts_page.has_next() else None
    page_start_index = (posts_page.number - 1) * paginator.per_page
    
    context = {
        'page': 'Home',
        'posts': posts_page,
        'next_page': next_page,
        'page_start_index': page_start_index,
    }
    
    if request.GET.get('paginator'):
        return render(request, 'a_posts/partials/_posts.html', context)  
    
    if request.htmx:
        return render(request, 'a_posts/partials/_home.html', context)
    return render(request, 'a_posts/home.html', context)


@login_required
def explore_view(request):
    posts = Post.objects.order_by('-created_at')
    context = {
        'page': 'Explore',
        'posts': posts,
    }
    if request.htmx:
        return render(request, 'a_posts/partials/_explore.html', context)
    return render(request, 'a_posts/explore.html', context)


@login_required
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


def post_page_view(request, pk=None):
    if not pk:
        return redirect('home')
    
    post = get_object_or_404(Post, uuid=pk)
    
    if post.author:
        author_posts = list(Post.objects.filter(author=post.author).order_by('-created_at'))
        index = author_posts.index(post)
        prev_post = author_posts[index - 1] if index > 0 else None
        next_post = author_posts[index + 1] if index < len(author_posts) - 1 else None
    else:
        author_posts = [ post ] 
        prev_post = next_post = None
    
    context = {
        'post' : post,
        'author_posts' : author_posts,
        'prev_post': prev_post,
        'next_post': next_post,
    }
    if request.htmx:
        return render(request, 'a_posts/partials/_postpage.html', context)
    return render(request, 'a_posts/postpage.html', context)


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, uuid=pk) 
    form = PostEditForm(instance=post)
    
    if post.author != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_page', pk)
        
    if request.GET.get("delete"):
        post.delete()
        return redirect('profile', request.user)
    
    context = {
        'form' : form,
        'post' : post
    }
    
    if request.htmx:
        return render(request, 'a_posts/partials/_post_edit.html', context)
    return redirect('post_page', pk)


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, uuid=pk)
    
    if request.htmx:
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    
    profile_user_likes = post.author.posts.aggregate(total_likes=Count('likes'))['total_likes']
           
    context = {
        'post': post,
        'profile_user_likes': profile_user_likes,
    }
    
    if request.GET.get("home"):
        return render(request, 'a_posts/partials/_like_home.html', context)
    if request.GET.get("postpage"):
        return render(request, 'a_posts/partials/_like_postpage.html', context)
    
    return redirect('post_page', pk)
