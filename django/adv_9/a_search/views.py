from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Q, Count

User = get_user_model()

def search(request):
    query = request.GET.get("q")
    
    users = User.objects.none()
    
    if query and len(query) >= 2:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(name__icontains=query) |
            Q(bio__icontains=query)
        ).order_by('username')
        
    context = {
        "users": users,
    }
    
    if request.htmx:
        return render(request, 'a_search/partials/_search_page.html', context)
    return render(request, "a_search/search_page.html", context)


def search_suggestions(request):
    query = request.GET.get("q")
    
    user_suggestions = User.objects.none()
    
    if query and len(query) >= 2: 
        user_suggestions = User.objects.filter(
            Q(username__icontains=query) |
            Q(name__icontains=query) | 
            Q(bio__icontains=query)
        ).annotate(followers_count=Count('is_followed', distinct=True)).order_by('-followers_count')[:5]
        
    context = {
        'user_suggestions': user_suggestions,
    }
    
    return render(request, "a_search/partials/_search_suggestions.html", context)
