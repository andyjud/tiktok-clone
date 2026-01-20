from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'input-field','placeholder': '#tags - separated by a space', 'maxlength': '80'}))
    file = forms.FileField() 
    
    class Meta:
        model = Post
        fields = ['body']
        
        
class PostEditForm(forms.ModelForm):
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'input-field','placeholder': '#tags - separated by a space', 'maxlength': '80'}))
    
    class Meta:
        model = Post
        fields = ['body']
        widgets = {
                'body' : forms.Textarea(attrs={'class': 'input-field resize-none','rows':2, 'placeholder': 'Add a caption here...', 'maxlength': '80'}),
            }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance.pk:
            tag_objs = self.instance.tags.all()
            tags = [str(tag) for tag in tag_objs] 
            if tags:
                self.initial['tags'] = " ".join(tags)
            else:
                self.initial['tags'] = ""