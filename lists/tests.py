from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from ..lists.models import Item
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from ..lists.views import home_page
# Create your tests here.

class HomePageTest(TestCase):
    def test_users_home_template(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response,'home.html')


    def test_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response=self.client.get('/')

        self.assertIn('itemey 1',response.content.decode())

        self.assertIn('itemey 2',response.content.decode())

class  ItemModelTest(TestCase):
    def test_saving_and_retrieving_item(self):
        first_item=Item()
        first_item.text='The first (ever) list item'
        first_item.save()

        second_item=Item()
        second_item.text='Item the second'
        second_item.save()

        saved_items=Item.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_saved_item=saved_items[0]
        second_saved_item=saved_items[1]
        self.assertEqual(first_saved_item.text,'The first (ever) list item')
        self.assertEqual(second_item.text,'Item the second')

class   ListViewTest(TestCase):
    def test_uses_list_template(self):
        response=self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response,'list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response=self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response,'itemey 1')
        self.assertContains(response,'itemey 2')
class   NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new',data={'item_text':'A new list item'})
        self.assertEqual(Item.objects.count(),1)#检查是否把一个新的item对象存入数据库，
        # object.count（）是object.all（）.count（）的简写模式
        new_item=Item.objects.first()#object.first（）等价于object.all()[0]
        self.assertEqual(new_item,'A new list item')#检查待办事项的文本是否正确
    def test_redirects_after_POST(self):
        response=self.client.post('/lists/new',data={'item_text':'A new list item'})
        self.assertEqual(response.status_code,302)
        self.assertEqual(response['location'],'/lists/the-only-list-in-the-world/')
        self.assertRedirects(response,'/lists/the-only-list-in-the-world/')