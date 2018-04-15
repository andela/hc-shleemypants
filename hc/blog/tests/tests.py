from django.test import TestCase
from hc.test import BaseTestCase
from django.contrib.auth.models import User
from .models import Post, PostsCategory, Comment
from django.shortcuts import reverse
from django.utils import timezone


"""
    All our tests will be in this file and first we initialize all the reusable variables in the setup function
"""
class BlogPostsCategories(BaseTestCase):
    def setUp(self):
        self.client.login(username="alice@example.org", password="password")
        self.category = PostsCategory(title='Artificial intelligence')
        self.category.save()
        self.blog = Post(title='Django newbies', content='Welcomes all newbies to django', 
                        category=self.category)
        self.blog.save()

    
    def test_create_blog(self):
        url = reverse('blogs:hc-category')
        blog = BlogPosts.objects.filter(title='Django newbies').first()
        self.assertEqual('Django newbies', blog.title)


    def test_create_category(self):
        url = reverse('blogs:hc-category')
        data = {'create_category-title': ['read'], 'create_category': ['']}
        response = self.client.post(url, data)
        category = PostsCategory.objects.filter(title='read').first()
        self.assertEqual('read', category.title)


    def test_home_page_returns_all_categories(self):
        url = reverse('blogs:hc-category')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/view_blogs.html')