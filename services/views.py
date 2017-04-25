from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth,redirects   #used auth import  for authentication--eish not sure about redirects yet
import datetime#import for date and time functions
from .models import members,victims ,users,groups# importing the members modules so can have all the properties
import random#random number import
import string#letter generator import
#------email imports----------------
import smtplib, hashlib
import email.utils
from email.mime.text import MIMEText
#-------end email imports-----------

def index(request):#INDEx page view
    print (request.session.get('login_session'))
    print ('printing')
    return render(request,'services/index.html')

def auth_view(request):
    username=request.POST.get('username', '')
    password=request.POST.get('password', '')
    #password=hashlib.md5(passwrd.encode('utf-8')).hexdigest()

    user = auth.authenticate(username=username, password=password)
    login_session=request.session.get('login_session', False)
    #var for sessions
    msg='' #this will hold the error message if there us one
    print('USERNAME'+ username)
    print('session' + str(login_session))
    memberlist=members.objects.all()

    for mem in memberlist:
        print (mem.username+""+mem.password)
        if mem.username==username and mem.password==password:
            #auth.login(request,user)#log user in using build in auth.login method
            request.session['login_session']=True
            request.session['user_id']=mem.id
            print(request.session.get('user_id'))
            return HttpResponseRedirect('/dash/')
        else:
            msg = "something wrong"
            return HttpResponseRedirect('/index/', {'errormsg': msg})  # ahh eish have to make this work

"""def loggedin_view(request):
    #login_session = request.session['login_session']
    if request.session['login_session']==True:
        return HttpResponseRedirect('/dash/',{'fname':'alex', 'surname':'Rama'})
    else:
        return HttpResponseRedirect('/index/')"""

def logout_view(request):
    try:
        del request.session['login_session']
        print('p1'+str(request.session['login_session']))
        auth.logout(request)
    except KeyError:
        pass
    for keys in request.session.keys():
        print('p2'+keys)
    return HttpResponseRedirect('/index/')

def register_view(request):#display the registration page
    #login_session = request.session['login_session']
    #if login_session == True:

   # else:
    #    return HttpResponseRedirect('/index/')
    if request.session.get('login_session',False)==False:
        return render(request, 'services/register.html')
    else:
        return HttpResponseRedirect('/dash/')

def registered_view(request):#when you click sign up button it goes to done registring page

    if request.session.get('login_session',False)==False:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        first_name = request.POST.get('firstname', '')
        last_name = request.POST.get('surname', '')
        email = request.POST.get('email', '')
        organization = request.POST.get('organization', '')
        membership = request.POST.get('membership', '')

        #hash_pass = hashlib.md5(password.encode('utf-8')).hexdigest()
        context = {'username': username, 'fname': first_name, 'surname': last_name,
                   'email': email}  # storing inputs here for such and such

        today = datetime.datetime.now().date()  # getting today date without time

        new_user = members(username=username, password=password, first_name=first_name, last_name=last_name,
                           email=email,
                           organization=organization, membership=membership, register_date=today)
        new_user.save()
        #registration_email(email, username)
        return render(request, 'services/registered.html', context)
    else:
        return HttpResponseRedirect('/index/')

def registration_email(new_user,username):#lets send an email after a user registers

    # Create the message
    msg = MIMEText('Welcome to the site '+ username+'click on the link below to confirm your email address')
    msg['To'] = email.utils.formataddr(('Recipient', new_user))
    msg['From'] = email.utils.formataddr(('Fisher Man', 'srv101.mail@gmail.com'))
    msg['Subject'] = 'Welcome to the site '+ username

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login('srv101.mail@gmail.com', 'thanyani12')
    server.set_debuglevel(True)  # show communication with the server
    try:
        server.sendmail('alexramantswana@gmail.com', [new_user], msg.as_string())
    finally:
        server.quit()

def attack_email(victim,username,random_id):#lets send an email to a single user

    # Create the message
    msg = MIMEText('Hello '+ username+' click on the link below to collect your million bucks\n\n http://127.0.0.1:8000/gophish/hooked/'+str(random_id)+'/ >Claim Prize</a></body></html> Now\n before its too late')
    msg['To'] = email.utils.formataddr(('Recipient', victim))
    msg['From'] = email.utils.formataddr(('Fisher Man', 'alexramantswana@gmail.com'))
    msg['Subject'] = 'Welcome to the site '+ username

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login('alexramantswana@gmail.com', 'thanyani12')
    server.set_debuglevel(True)  # show communication with the server
    try:
        server.sendmail('alexramantswana@gmail.com', [victim], msg.as_string())
    finally:
        server.quit()

def dash_view(request):#displays the dashboard
    #print(request.session['login_session'])
    #login_session = request.session['login_session']
    if request.session.get('login_session',False)==True:
        print (request.session['login_session']),'hola'

        mem_id=request.session.get('user_id')#users id stored session in login/auth view
        member = members.objects.get(id=mem_id)#

        victims_model = victims.objects.all()  # get victims list of the logged in user
        print(member)

        return render(request, 'services/dash.html', {'victims_model': victims_model,'fname':member.first_name,'lname':member.last_name })
    else:
        return HttpResponseRedirect('/index/')


def phish_view(request):#logic for quick phishing attack
    victim_email=request.POST.get('email','')
    victim_name=request.POST.get('username', '')

    random_id=random.randint(1,1000)#generate random id
    hash_id = hashlib.md5(repr(random_id).encode('utf-8')).hexdigest()

    """letter = random.choice(string.ascii_letters) + "" + random.choice(string.ascii_letters) + random.choice(
    string.ascii_letters) + "" + random.choice(string.ascii_letters)
    hash_id = hashlib.md5(letter.encode('utf-8')).hexdigest()"""
    mychars = ''
    for i in range(16):#this is for generating random characters for user tracking
        mychars = mychars + random.choice(string.ascii_letters)

    #str_hash=str(hash_id)
    #hash_id = hashlib.md5(random_id.encode('utf-8').hexdigest())

    #attack_email(victim_email,victim_name,random_id)#phishing email

    today = datetime.datetime.now().date()#obvious
    phish_url='http://139.162.178.79:8000/gophish/hooked/'+mychars+'/'#url to be inside the email
    mem_id = request.session.get('user_id')  # users id stored session in login/auth view
    victim=victims(fullname=victim_name,useremail=victim_email,date_of_attack=str(today),url=phish_url,auto_id=mychars,predator_id=mem_id)#record victim details in db
    victim.save()#save victim in db

    return HttpResponseRedirect('/dash/')

def record_click_view(request,user_id):
    print('we in phish view before try')
    status="compromised"
    victim=victims.objects.get(auto_id=user_id)
    victim.vulnerable=status
    victim.date_of_compromise=str(datetime.datetime.now())
    victim.save()
    return render(request,'services/errorpage.html')


def users_view(request):
    return render(request,'services/user.html')

def new_user_view(request):#display the page for adding new users
    if request.session.get('login_session', False) == True:
        group_model=groups.objects.all()
        return render(request,'services/new_user.html',{"group_model":group_model})
    else: return HttpResponseRedirect('/index/')

def user_list_view(request):#displays the users page

    if request.session.get('login_session',False)==True:
        user_list = users.objects.all()
        return render(request, 'services/users.html', {'user_list': user_list})
    else:
        return HttpResponseRedirect('/index/')
def add_user_view(request):#adds a new user to the list
    first_name=request.POST.get('fname','')
    last_name=request.POST.get('lname','')
    email=request.POST.get('email','')
    group=request.POST.get('DropDownGroup','')
    group_id=0


    if group=='':
        group_id=group_id
    elif group != '':
        group_id = group.objects.id(group_name=group)


    random_id=random.randint(1,100)#generate random id
    today = datetime.datetime.now().date()

    new_user=users(group_id=group_id,first_name=first_name,last_name=last_name,email=email,date_of_attack=today,auto_id=random_id)
    new_user.save()

    return HttpResponseRedirect('/user_list/')

def btngroup_view(request):
    if request.POST.get('newuser'):
        return (request,'services/new_user.html')
    elif request.POST.get('import'):
        return render(request,'user_.html')
    elif request.POST.get('export'):
        return render(request,'services/users.html')
    else:
        return render(request,'services/errorpage.html')

def showme(request):
    print(request.session.get('login_session'))

def save(request):#saves the url report list
    filename=request.POST.get("filename", 'report.txt')
    data=victims.objects.all()
    for item in data:
        write_urls("Name: "+item.fullname+" Email: "+item.useremail+" Status: "+item.vulnerable+" URL: "+item.url,filename)
    return  HttpResponseRedirect('/dash/')
def write_urls(data,filename):
    file=open("C:\\Users\\Joe\\Documents\\"+filename,"a+")
    file.write(str(data) + "\n")

def reset_view(request,user_id):
    victim = victims.objects.get(auto_id=user_id)
    victim.vulnerable = "still safe"
    victim.date_of_compromise = str(datetime.datetime.now())
    victim.save()
    return HttpResponseRedirect('/dash/')