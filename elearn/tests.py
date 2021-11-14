from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
import os

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        # create profile
        self.s1 = Profile.objects.create(username="admin1",password='123456',firstname="AAA",lastname="BBB",email="A@mail.com")
        self.s2 = Profile.objects.create(username="admin2",password='123456',firstname="CCC",lastname="DDD",email="C@mail.com")

        # create user
        self.user1 = User.objects.create_user(username='AAA', password='123456', email='A@mail.com')
        self.user2 = User.objects.create_user(username='CCC', password='123456', email='C@mail.com')
        self.user3 = User.objects.create_superuser(username='admin', password='1234', email='admin@mail.com')

        # create subject
        self.subject1 = SubjectSubscribe.objects.create(subject="1111", subjectid="cn111" )
        self.subject2 = SubjectSubscribe.objects.create(subject="2222", subjectid="cn222" )
        self.subject3 = SubjectSubscribe.objects.create(subject="3333", subjectid="cn333")

        # create comment
        # self.comment1 = Comments

        # # path url
        self.index_url = reverse('index')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.signup_url = reverse('signup')
        self.courselist_url = reverse('courselist')
        self.createsubject_url = reverse('createsubject')
        self.about_url = reverse('about')
        self.signup_url = reverse('signup')
        self.searchcourse_url = reverse('searchcourse')
        # self.bookcourselist_url = reverse('bookcourselist')
        # self.eachsubject_url = reverse('eachsubject')
        # self.commenteachsubject_url = reverse('commenteachsubject')
        self.editprofile_url = reverse('editprofile')
        # Client
        self.client = Client()
    
    def redirect(self , res):
        return dict(res.items())['Location']


    # กรณีที่ล็อคอิน ผิดพลาด ต้องไม่สามารถเข้าสู่ระบบได้
    def test_login_1(self):
        """ check in test_login_1!! """
        response = self.client.post(self.login_url,{'username':'5555','password':'5555'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'elearn/login.html')
        self.assertEqual(response.context["message"],"Invalid username or password.")


    # กรณีที่สมัครเป็นสมาชิกแล้ว ต้องสามารถเข้าสู่ระบบได้
    def test_login_2(self):
        """ check in test_login_2!! """
        user = User.objects.filter(email=self.user2.email).first()
        user.is_active=True
        user.save()
        response = self.client.post(self.login_url,{'username':user,'password':'123456'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'elearn/index.html')


    # กรณีที่ล็อคอินเป็น แอดมิน ต้องเข้าสู่ระบบได้
    def test_login_3(self):
        """ check in test_login_3!! """
        user = User.objects.filter(email=self.user3.email).first()
        user.is_active=True
        user.save()
        response = self.client.post(self.login_url,{'username':user,'password':'1234'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'elearn/index.html')

    # กรณีออกจากระบบ
    def test_logout(self):
        """ check in test_logout!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'elearn/index.html')
        self.assertEqual(response.context["message"],"Log out.")

    # กรณีต้องการตรวจสอบรายวิชาที่เปิดอยู่
    def test_coureslist(self):
        """ check courelist """
        self.client.force_login(self.user1)
        response = self.client.post(self.courselist_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'elearn/courselist.html')
        self.assertEqual(len(response.context["list"]),3)
    
    #กรณีค้นหาวิชาเรียนแล้วพบ
    def test_searchcourse_1(self):
        """ check in test_searchcourse_1 """
        self.client.force_login(self.user1)
        response = self.client.get(self.searchcourse_url,{'subjectid':'cn',})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/courselist/")
        # self.assertTemplateUsed(response , 'elearn/courselist.html')
        # self.assertEqual(len(response.context["list"]),3)
        
    #กรณีค้นหาวิชาเรียนแล้วไม่พบ
    def test_searchcourse_2(self):
        """ check in test_searchcourse_2 """
        self.client.force_login(self.user1)
        response = self.client.get(self.searchcourse_url,{'subjectid':'tu',})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/courselist/")
        # self.assertTemplateUsed(response , 'elearn/courselist.html')
        # self.assertEqual(len(response.context["list"]),0)
        
        
        
    # กรณีเพิ่มวิชาสำเร็จ
    def test_create_subject_1(self):
        """ check in test_add_subject_1!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.createsubject_url,{'subject':'test','subjectid':'cn999'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/courselist/")

    กรณีเพิ่มวิชาไม่สำเร็จ
    def test_create_subject_2(self):
        """ check in test_add_subject_2!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.createsubject_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'elearn/createsubject.html')

    # กรณีเข้าถึง about
    def test_about(self):
        """ check in test_about!! """
        response = self.client.post(self.about_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'elearn/about.html')

    # กรณี signup สำเร็จ
    def test_signup_1(self):
        """ check in test_signup_1 """
        response = self.client.post(self.signup_url,{'username':'teststudent','first_name':'firmino','last_name':'bobby','password1':'123admin123','password2':'123admin123', 'email':'test@mail.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'elearn/index.html')
        self.assertEqual(response.context["message"],"Registration successful.")

    # กรณี signup ไม่สำเร็จ
    def test_signup_2(self):
        """ check in test_signup_2 """
        response = self.client.post(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'elearn/signup.html')

    # กรณี subscribe course สำเร็จ
    def test_bookcourselist_1(self):
        """ check in test_bookcourselist_1 """
        self.client.force_login(self.user1)
        response = self.client.get(f'/courselist/{self.subject1.id}')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/courselist/")

    #กรณียกเลิกการ subscribe วิชานั้นๆ
    def test_bookcourselist_2(self):
        """ check in test_bookcourselist_2 """
        self.client.force_login(self.user1)
        response = self.client.get(f'/courselist/{self.subject1.id}')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/courselist/")
        response = self.client.get(f'/courselist/{self.subject1.id}')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/courselist/")

    
        
        
    # กรณี ตรวจสอบแต่ละวิชา
    def test_eachsubject_1(self):
        """ check in test_eachsubject_1 """
        self.client.force_login(self.user1)
        response = self.client.get(f'/courselists/{self.subject1.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'elearn/eachsubject.html')
        # self.assertEqual(len(list(response.context["subject"])),1)
        print("context:",response.context["subject"])
        # self.assertEqual(len(list(response.context["comments"])),0)
        # self.assertEqual(len(list(response.context["videos"])),0)
        # self.assertEqual(len(list(response.context["files"])),0)

    กรณี comment ในวิชาต่างๆ
    def test_commenteachsubject_1(self):
        """ check in test_commenteachsubject_1 """
        self.client.force_login(self.user1)
        response = self.client.get(f'/addcomment/{self.subject1.id}',{'body':'comments'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'elearn/eachsubject.html')
        self.assertEqual(len(response.context["subject"]),1)
        self.assertEqual(len(response.context["comments"]),1)
        self.assertEqual(len(response.context["videos"]),0)
        self.assertEqual(len(response.context["files"]),0)

    #กรณีแก้ไขบัญชีผู้ใช้สำเร็จ
    def test_editprofile_1(self):
        self.client.force_login(self.user1)
        response = self.client.post(self.editprofile_url,{'first_name':'ZZZ','last_name':'BBB','password':'123456'})
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(self.user1.first_name,'ZZZ')
        print(self.user1)
        self.assertEqual(self.redirect(response), "/")

    # กรณีแก้ไขบัญชีผู้ใช้ไม่สำเร็จเนื่องจากไม้ได้ login
    def test_editprofile_2(self):
        response = self.client.post(self.editprofile_url,{'first_name':'ZZZ','last_name':'BBB','password':'123456'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/")

    
