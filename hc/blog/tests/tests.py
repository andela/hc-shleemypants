from django.test import TestCase
from hc.test import BaseTestCase
from django.contrib.auth.models import User
from ..models import Post, PostsCategory, Comment
from django.shortcuts import reverse
from django.utils import timezone


"""
    All our tests will be in this file and first we initialize all the reusable variables in the setup function
"""
class BlogTestCase(BaseTestCase):
    def setUp(self):
        
        res = self.client.login(username="alice@example.org", password="password")
        self.category = PostsCategory(title='Artificial intelligence')
        self.category.save()
        self.user = User(username="alice", email="alice@example.org")
        self.user.save()
        self.blog = Post(title='Django newbies', body='Welcomes all newbies to django', 
                        category=self.category, author= self.user)
        self.blog.save()

    
    def test_create_blog(self):
        url = reverse('blog:hc-category')
        blog = Post.objects.filter(title='Django newbies').first()
        self.assertEqual('Django newbies', blog.title)


    def test_create_category(self):
        url = reverse('blog:hc-category')
        data = {'create_category-title': ['learn'], 'create_category': ['']}
        response = self.client.post(url, data)
        category = PostsCategory.objects.filter(title='learn').first()
        self.assertEqual('learn', category.title)


    def test_home_page_returns_all_categories(self):
        url = reverse('blog:hc-category')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/view_blogs.html')

    def test_create_category_form_invalid(self):
        url = reverse('blog:hc-category')
        data = {'create_category-title': [''], 'create_category': ['']}
        response = self.client.post(url, data)
        self.assertRedirects(response, '/blog/')
        self.assertEqual(response.status_code, 302)

   
    def test_if_get_redirect(self):
        url = reverse('blog:hc-category')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/view_blogs.html')