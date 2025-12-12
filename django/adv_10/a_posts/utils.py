import re
from .models import Tag
from django.db.models import F

def process_tags(post, input_tags=None):
    # remove counts and clear all the tags from the post
    for tag in post.tags.all():
        Tag.objects.filter(pk=tag.pk).update(count=F('count') - 1)
    post.tags.clear()
    
    # add tags and counts
    if input_tags is not None:
        tags = set(re.findall(r"#(\w+)", input_tags.lower())) 
        for name in tags: 
            tag, created = Tag.objects.get_or_create(name=name)
            post.tags.add(tag)
            Tag.objects.filter(pk=tag.pk).update(count=F('count') + 1)
            
    # delete tags with 0 counts  
    Tag.objects.filter(count__lte=0).delete()
        