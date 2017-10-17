from django.db import models
from datetime import datetime

# Create your models here.
class members(models.Model):
    id = models.AutoField(primary_key=True)
    username=models.CharField(max_length=100)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    organization=models.CharField(max_length=100)
    confirm_id=models.CharField(max_length=16,default='0')
    confirmed =models.CharField(max_length=100,default='0')
    register_date = models.CharField(max_length=100, default=datetime.now())
    def __str__(self):
        return self.username+' '+self.last_name



class quick_attack(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100, default='')
    useremail=models.CharField(max_length=100)
    sent_date=models.CharField(max_length=100,default='')
    url_id=models.CharField(max_length=16,default='')
    long_url=models.CharField(max_length=100,default='')
    short_url=models.CharField(max_length=100,default='')
    status = models.CharField(max_length=11, default='Safe')
    member_id=models.ForeignKey('members',on_delete=models.CASCADE,default=0)
    group_id = models.ForeignKey('groups',on_delete=models.CASCADE,default=0)

    def __str__(self):
        return self.fullname

class quick_attack_clicks(models.Model):
    click_id=models.AutoField(primary_key=True)
    long_url = models.CharField(max_length=300, default='')
    short_url = models.CharField(max_length=300, default='')
    ip_add=models.CharField(max_length=30, default='')
    date_of_compromise = models.CharField(max_length=100, default='')
    member_id = models.ForeignKey('members', on_delete=models.CASCADE, default=0)
    user_id = models.ForeignKey('quick_attack', on_delete=models.CASCADE, default=0)

class campaign(models.Model):
    campaign_id=models.AutoField(primary_key=True)
    campaign_name=models.CharField(max_length=100,default='')
    campaign_desc=models.CharField(max_length=300,default='')
    date_created=models.CharField(max_length=100,default=datetime.now())
    member_id =models.ForeignKey('members',on_delete=models.CASCADE,default=0)

    def __str__(self):
        return self.campaign_name

class groups(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name=models.CharField(max_length=100,default='')
    group_description = models.CharField(max_length=100, default='')
    created_date = models.CharField(max_length=100, default=datetime.now())
    campaign_id= models.ForeignKey('campaign',on_delete=models.CASCADE,default=0)
    member_id=models.ForeignKey('members',on_delete=models.CASCADE,default=0)

    def __str__(self):
        return self.group_name

class userss(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100, default='')
    useremail=models.CharField(max_length=100)
    sent_date=models.CharField(max_length=100,default=datetime.now())
    url_id=models.CharField(max_length=16,default='')
    long_url=models.CharField(max_length=100,default='')
    short_url=models.CharField(max_length=100,default='')
    status = models.CharField(max_length=11, default='Safe')
    member_id=models.ForeignKey('members',on_delete=models.CASCADE,default=0)
    group_id = models.ForeignKey('groups',on_delete=models.CASCADE,default=0)

    def __str__(self):
        return self.fullname

class landin_page(models.Model):
    page_id = models.AutoField(primary_key=True)
    page_name=models.CharField(max_length=100,default='')
    page_content = models.CharField(max_length=1000000000000, default='')
    page_upload=models.FileField(default='No Image File')
    member_id=models.ForeignKey('members',on_delete=models.CASCADE,default=0)

class user_groups(models.Model):
    user_group_id = models.AutoField(primary_key=True)
    group_id = models.ForeignKey('groups', on_delete=models.CASCADE, default=0)
    member_id = models.ForeignKey('members', on_delete=models.CASCADE, default=0)
    user_id = models.ForeignKey('quick_attack', on_delete=models.CASCADE, default=0)

class sending_profiles(models.Model):
    profile_id=models.AutoField(primary_key=True)
    profile_name=models.CharField(max_length=100,default='')
    profile_email = models.CharField(max_length=100, default='')
    profile_password=models.CharField(max_length=100,default='')
    profile_server=models.CharField(max_length=100,default='')
    profile_port = models.IntegerField(max_length=10, default=0)
    profile_header = models.CharField(max_length=100, default='')
    created_date = models.CharField(max_length=100, default=datetime.now())
    campaign_id= models.ForeignKey('campaign',on_delete=models.CASCADE,default=0)
    member_id=models.ForeignKey('members',on_delete=models.CASCADE,default=0)
