from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse
from .forms import PostForm, PostEditForm
from .models import Post, Comment


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
    
    if request.method == "POST": 
        body = request.POST.get('comment')
        if body:
            Comment.objects.create(
                author=request.user,
                post=post,
                body=body
            )
            context = {
                'post': post
            }
            return render(request, 'a_posts/partials/comments/_comment_loop.html', context)
    
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


@login_required
def bookmark_post(request, pk):
    post = get_object_or_404(Post, uuid=pk)
    
    if request.htmx:
        if post.bookmarks.filter(id=request.user.id).exists():
            post.bookmarks.remove(request.user)
        else:
            post.bookmarks.add(request.user)
            
    context = {
        'post': post,
    }
    
    if request.GET.get("home"):
        return render(request, 'a_posts/partials/_bookmark_home.html', context)
    if request.GET.get("postpage"):
        return render(request, 'a_posts/partials/_bookmark_postpage.html', context)
    
    return redirect('post_page', pk)


@login_required
def comment(request, pk):
    if not request.htmx:
        return redirect('home')

    comment = get_object_or_404(Comment, uuid=pk) 
    
    parent_comment = comment 
    while parent_comment.parent_comment:
        parent_comment = parent_comment.parent_comment
    
    if request.method == 'POST':
        body = request.POST.get('reply')
        if body:
            Comment.objects.create(
                author=request.user,
                post=comment.post,
                parent_comment=parent_comment,
                body=body
            )
         
    context = {
        'comment': parent_comment,
    }
    
    if request.GET.get("hide_replies"):
        return render(request, 'a_posts/partials/comments/_button_view_replies.html', context)
    if request.GET.get("reply_form"):
        return render(request, 'a_posts/partials/comments/_form_add_reply.html', context)
    
    return render(request, 'a_posts/partials/comments/_reply_loop.html', context)


@login_required
def comment_delete(request, pk):
    if not request.htmx:
        return redirect('home')
    
    comment = get_object_or_404(Comment, uuid=pk) 
    if comment.author != request.user:
        return HttpResponse()

    if request.method == 'POST':
        post = comment.post
        comment.delete()
        
        comment_count = post.comments.count()
        new_count = f"<div hx-swap-oob='innerHTML' id='comment_count'>{comment_count}</div>"
        return HttpResponse(new_count)

    context = {
        'comment': comment
    }
    return render(request, 'a_posts/partials/comments/_form_delete_comment.html', context)



@login_required
def like_comment(request, pk):
    if not request.htmx:
        return redirect('home')
    
    comment = get_object_or_404(Comment, uuid=pk) 

    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)

    context = {
        'comment': comment
    }
    return render(request, 'a_posts/partials/comments/_button_like_comment.html', context)
