from django import forms
from .models import PostsCategory, Post, Comment

# forms for the blog

class BlogPostsCategoryForm(forms.ModelForm):
    class Meta:
        model = PostsCategory
        fields = ('title',)

class BlogPostsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category', 'title','body')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)