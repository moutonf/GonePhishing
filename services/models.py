from django.db import models


class members(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    organization=models.CharField(max_length=100)
    membership =models.CharField(max_length=100)
    register_date=models.CharField(max_length=100)

    def __str__(self):
        return self.username

class victims(models.Model):
    #id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100, default='')
    useremail=models.CharField(max_length=100)
    date_of_attack=models.CharField(max_length=100)
    date_of_compromise = models.CharField(max_length=100,default='')
    duration=models.CharField(max_length=100,default='')
    vulnerable=models.CharField(max_length=2,default='Still Safe')
    auto_id=models.IntegerField(default=0)

    def __str__(self):
        return self.fullname

class groups(models.Model):
    group_name=models.CharField(max_length=100)
    group_description=models.CharField(max_length=200)

    def __str__(self):
        return self.group_name

class users(models.Model):
    group_id=models.ForeignKey(groups, on_delete=models.CASCADE,default=0)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    date_of_attack=models.CharField(max_length=100)
    date_of_compromise = models.CharField(max_length=100,default='')
    duration=models.CharField(max_length=100,default='')
    vulnerable=models.CharField(max_length=2,default='Still Safe')
    auto_id=models.IntegerField(default=0)

    def __str__(self):
        return self.first_name