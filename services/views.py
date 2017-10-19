from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth,redirects   #used auth import  for authentication--eish not sure about redirects yet
from _datetime import datetime#import for date and time functions
from .models import *
## ,victims ,users,groups, emailss,drafts# importing the members modules so can have all the properties
import random#random number import
import string#letter generator import
#------email imports----------------
import smtplib, hashlib
import email.utils
from email.mime.text import MIMEText
#import os
#-------end email imports-----------

#----------bitly--------------------
import requests
import subprocess
import json
import os,datetime
#--------end bitly--------------------
#methods to add----------
#return todays date
#return user id
#return url
#reuturn mychars
#generate url
#url shotner
#send email(what is email for/(reg,quick att,emailtemp)from sender, to, blah blahblah)

def todays():
     time=str(datetime.datetime.now())
     return time[:-7]

def  get_member_id(request):
    mem_id = request.session.get('user_id')  # users id stored session in login/auth view
    member_id=members.objects.get(id=mem_id)
    return member_id.id

def url_shortner(long_url):
    #token=os.system('C:\\curl-7.54.0-win64-mingw\\bin\\curl -u "thanyani12:Thanyani12!" -X POST "https://api-ssl.bitly.com/oauth/access_token')
    #token = subprocess.call('curl -u "thanyani12:Thanyani12!" -X POST "https://api-ssl.bitly.com/oauth/access_token',shell=True)
    # print(token2)

    token='472c63e603060caf8f0124d0044551896d4abcf4'
    query_params = {'access_token': token,
                    'longUrl': long_url}

    endpoint = 'https://api-ssl.bitly.com/v3/shorten'
    response = requests.get(endpoint, params=query_params, verify=False)

    data = json.loads(response.content)
    #bityl_url=data['data']['url']


    return data['data']['url']


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
            if mem.confirmed=='0':
                #auth.login(request,user)#log user in using build in auth.login method
                request.session['login_session']=True
                request.session['user_id']=mem.id
                print(request.session.get('user_id'))
                return HttpResponseRedirect('/dash/')
            else:
                return HttpResponseRedirect('/not_confirmed/')
    msg = "something wrong"
    return HttpResponseRedirect('/index/', {'errormsg': msg})  # ahh eish have to make this work

def not_confirmed_view(request):
    return  render
"""def loggedin_view(request):
    #login_session = request.session['login_session']
    if request.session['login_session']==True:
        return HttpResponseRedirect('/dash/',{'fname':'alex', 'surname':'Rama'})
    else:
        return HttpResponseRedirect('/index/')"""
        #return HttpResponseRedirect('/index/', {'errormsg': msg})
#authentication logic---------------------------------------------------------------------------------------------------
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

def registered_view(request):#when you click sign up button it goes to done registering page

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
        member_list=members.objects.all()
        for member in member_list:
            if member.username==username:
                return HttpResponseRedirect('/register/',context)
            else:
                #today = datetime.datetime.now().date()  # getting today date without time
                mychars = ''
                for i in range(16):  # this is for generating random characters for user tracking
                    mychars = mychars + random.choice(string.ascii_letters)

                new_user = members(username=username, password=password, first_name=first_name, last_name=last_name,email=email,
                           organization=organization,confirme_id=mychars,register_date=todays())
                new_user.save()
                registration_email(email, username,mychars)
                return render(request, 'services/registered.html', context)
    else:
        return HttpResponseRedirect('/index/')

def registration_email(new_user,username,mychars):#lets send an email after a user registers
    # Create the message
    msg = MIMEText('Welcome to the site '+ username+'  click on the link below to confirm your email address\n\n '+'http://http://127.0.0.1:8000/confirm/'+mychars+'/')
    msg['To'] = email.utils.formataddr(('Recipient', new_user))
    msg['From'] = email.utils.formataddr(('Fisher Man', 'srv101.mail@gmail.com'))
    msg['Subject'] = 'Welcome to the site '+ username

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login('srv101.mail@gmail.com', 'Phishyphishy123')
    server.set_debuglevel(True)  # show communication with the server
    try:
        server.sendmail('alexramantswana@gmail.com', [new_user], msg.as_string())
    finally:
        server.quit()

def email_confirm(request,emial_id):
    memeber=members.objects.get(confirm_id=emial_id)
    memeber.confirmed='1'

#dashboard logic--------------------------------------------------------------------------------------------------------
def attack_email(victim_email,victim_name,url):#lets send an email to a single user

    # Create the message
    msg = MIMEText('Hello '+ victim_name+' click on the link below to collect your million bucks\n\n'+url+' To Claim PrizeNow\n before its too late')
    msg['To'] = email.utils.formataddr(('Recipient', victim_email))
    msg['From'] = email.utils.formataddr(('Fisher Man', 'alexramantswana@gmail.com'))
    msg['Subject'] = 'Welcome to the site '+ victim_name

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login('srv101.mail@gmail.com', 'Phishyphishy123')
    server.set_debuglevel(True)  # show communication with the server
    try:
        server.sendmail('alexramantswana@gmail.com', [victim_email], msg.as_string())
    finally:
        server.quit()
def dash_view(request):#displays the dashboard
    #print(request.session['login_session'])
    #login_session = request.session['login_session']
    if request.session.get('login_session',False)==True:
        print (request.session['login_session']),'hola'

        mem_id=request.session.get('user_id')#users id stored session in login/auth view
        member = members.objects.get(id=mem_id)#

        victims_model = quick_attack.objects.filter(member_id=member.id)  # get victims list of the logged in user
        #campaign_model=campaign.objects.filter(member_id=member)
        profile_model=sending_profiles.objects.filter(member_id=member)

        print(member)

        return render(request, 'services/dash.html', {'victims_model': victims_model,'fname':member.first_name,'lname':member.last_name,'profiles':profile_model })
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


    #today = datetime.now().date()#obvious
    phish_url='http://127.0.0.1:8000/gophish/hooked/'+mychars+'/'#url to be inside the email
    bitly_url=url_shortner(phish_url)
    #phish_url = 'http://139.162.178.79:8000/gophish/hooked/' + mychars + '/'  # url to be inside the email

    attack_email(victim_email,victim_name,bitly_url)#phishing email

    mem_id = request.session.get('user_id')  # users id stored session in login/auth view
    member_id=members.objects.get(id=mem_id)

    victim=quick_attack(fullname=victim_name,useremail=victim_email,sent_date=str(todays()),url_id=mychars,long_url=phish_url,short_url=bitly_url, member_id=member_id)#record victim details in db
    victim.save()#save victim in db

    return HttpResponseRedirect('/dash/')

def record_click_view(request,user_id):

    status="compromised"
    victim=quick_attack.objects.get(url_id=user_id)
    victim.status=status
    #victim.date_of_compromise=str(datetime.datetime.now())
    victim.save()

    mem_id = request.session.get('user_id')  # users id stored session in login/auth view
    member_id=members.objects.get(id=mem_id)


    #ip_add=os.environ["REMOTE_ADDR"]
    ip_add=request.environ['REMOTE_ADDR']
    owner=quick_attack.objects.get(id=victim.id)

    click_data=quick_attack_clicks(ip_add=ip_add,date_of_compromise=str(todays()),member_id=member_id,user_id=owner)
    click_data.save()
    return render(request,'services/errorpage.html')

def campaign_click_view(request,url_id):

    #change user status to compromised
    status="compromised"
    victim=userss.objects.get(url_id=url_id)
    victim.status=status
    victim.save()

    #mem_id = request.session.get('user_id')  # users id stored session in login/auth view

    #member_id=members.objects.get(id=int(victim.member_id))
    #ip_add=os.environ["REMOTE_ADDR"]
    ip_add=request.environ['REMOTE_ADDR']

    #owner=quick_attack.objects.get(id=victim.id)

    click_data=campaign_clicks(ip_add=ip_add,date_of_compromise=todays(),member_id=victim.member_id,user_id=victim)
    click_data.save()

    return render(request,'services/errorpage.html')

def detail_view(request,click_id):#dispays the detail view when u click details link in dashboard
    victim_details=quick_attack.objects.get(id=click_id)
    clicks=quick_attack_clicks.objects.filter(user_id=victim_details.id)

    return render(request,'services/details.html',{'click':clicks,'victims':victim_details})

def reset_view(request,user_id):
    victim = quick_attack.objects.get(id=user_id)
    victim.status = "Safe"
    today=str(datetime.now())
    date_time= today[:-5]
    victim.date_of_compromise =date_time
    victim.save()

    clicks_reset=quick_attack_clicks.objects.get(user_id=user_id)

    clicks_reset.delete()
    #
    # for clicks in clicks_reset:
     #   clicks.delete()

    return HttpResponseRedirect('/dash/')

def remove_view(request,click_id):
    clicks=quick_attack_clicks.objects.get(click_id=click_id)
    clicks.delete()
    #clicks=quick_attack_clicks.objects.all()
    #victim_details=quick_attack.objects.get(click_id=click_id)
    #return HttpResponseRedirect('/details/',{'click':clicks,'victims':victim_details})
    return  HttpResponseRedirect('/dash/')

#campaigns logic--------------------------------------------------------------------------------------------------------
def campaign_view(request):
    if request.session.get('login_session', False) == True:
        mem_id = request.session.get('user_id')  # users id stored session in login/auth view
        member_id=members.objects.get(id=mem_id)
        campaign_list = campaign.objects.filter(member_id=member_id.id).order_by('-date_created')
        return render(request,'services/campaign.html',{'campaigns':campaign_list})
    return HttpResponseRedirect('/index/')

def new_campaign_view(request):
    if request.session.get('login_session', False) == True:
        return render(request,'services/campaign_new.html')
    return HttpResponseRedirect('/index/')

def add_campaign_view(request):

    if request.session.get('login_session', False) == True:
        mem_id = request.session.get('user_id')  # users id stored session in login/auth view
        member_id=members.objects.get(id=mem_id)

        campaign_name=request.POST.get('campaign_name','')
        campaign_descr = request.POST.get('campaign_desc', '')

        new_campaign=campaign(campaign_name=campaign_name,campaign_desc=campaign_descr,date_created=todays(),member_id=member_id)
        new_campaign.save()


        return HttpResponseRedirect('/campaign/new/')
    return HttpResponseRedirect('/index/')

def save_campaign_view(request):
    if request.session.get('login_session', False) == True:

        mem_id = request.session.get('user_id')  # users id stored session in login/auth view
        member_id=members.objects.get(id=mem_id)

        campaign_name=request.POST.get('campaign_name','')
        campaign_descr = request.POST.get('campaign_desc', '')

        new_campaign=campaign(campaign_name=campaign_name,campaign_desc=campaign_descr,member_id=member_id)
        new_campaign.save()

        return HttpResponseRedirect('/campaign/')
    return HttpResponseRedirect('/index/')

def campaign_remove_view(request,campaign_id):
    if request.session.get('login_session', False) == True:
        camp=campaign.objects.get(campaign_id=campaign_id)
        camp.delete()
        return  HttpResponseRedirect('/campaign/')
    return HttpResponseRedirect('/index/')

def campaign_results_view(request,campaign_id):#dispays the detail view when u click details link in dashboard
    if request.session.get('login_session', False) == True:
        group_list = groups.objects.filter(campaign_id=campaign_id)
        #user_list=userss.objects.filter(group_id=)
        print(campaign_id)
        request.session['campaign_id'] = campaign_id
        return render(request,'services/campaign_results.html',{'group_list':group_list,'campaign_id':campaign_id})
    return HttpResponseRedirect('/index/')

def campaign_remove_group_view(request,campaign_id,group_id):
    if request.session.get('login_session', False) == True:
        camp=campaign.objects.get(campaign_id=campaign_id)
        group=groups.objects.get(group_id=group_id)
        group.delete()
        return  HttpResponseRedirect('/campaign/results/'+campaign_id+'/',)
    return HttpResponseRedirect('/index/')

def campaign_config_view(request,campaign_id):#dispays the detail view when u click details link in dashboard
    if request.session.get('login_session', False) == True:
        group_list = groups.objects.filter(campaign_id=campaign_id)
        profile_model = sending_profiles.objects.filter(member_id=get_member_id(request))
        landing_pages=landin_page.objects.filter(member_id=get_member_id(request))
        return render(request,'services/campaign_config.html',{'group_list':group_list,'campaign_id':campaign_id,'profiles':profile_model})
    return HttpResponseRedirect('/index/')

def campign_users_view(request,group_id): #display list of users
    if request.session.get('login_session', False) == True:
        #mem_id = request.session.get('user_id')  # users id stored session in login/auth view
        #member_id = members.objects.get(id=mem_id)

        g_id=groups.objects.get(group_id=group_id)
        user_list = userss.objects.filter(member_id=get_member_id(request),group_id=g_id)
        return render(request,'services/campaign_users.html',{'user_list':user_list,'group_name':g_id.group_name,'group_id':g_id.group_id})

    return HttpResponseRedirect('/index/')
def campign_users_detail_view(request,group_id,user_id):
    #group=groups.objects.get(group_id=group_id)
    usr_list=userss.objects.filter(id=user_id, group_id=group_id)
    click_details=campaign_clicks.objects.filter(user_id=user_id)

    return render(request,'services/campaign_details_users.html',{'details':usr_list,'clicks':click_details})

def campaign_start_view(request,campaign_id):
    target_campaign=campaign.objects.get(campaign_id=campaign_id)
    target_group=groups.objects.filter(campaign_id=target_campaign)
    target_users=[]

    for group in target_group:
        #print("Group name: "+str(group))
        target_users=userss.objects.filter(group_id=group)
        for user in target_users:
            #print('users :' + str(user))
            mychars = ''
            for i in range(16):  # this is for generating random characters for user tracking
                mychars = mychars + random.choice(string.ascii_letters)
            #print('mychars :'+ mychars)

            long_url = 'http://127.0.0.1:8000/gophish/hook/' + mychars + '/'  # url to be inside the email
            bitly_url = url_shortner(long_url)
            user.long_url=long_url
            user.short_url=bitly_url
            user.url_id=mychars

            '''print(long_url)
            print(bitly_url)
            print(user.long_url)
            print(user.short_url)'''
            user.save()
            attack_email(user.useremail,user.fullname, user.short_url)
    return HttpResponseRedirect('/campaign/results/'+str(campaign_id)+'/')



def campaign_stop_view(request,campaign_id):
    print()

def import_group_view(request,campaign_id):
    if request.session.get('login_session', False) == True:

        group_model=groups.objects.exclude(campaign_id=campaign_id).filter(member_id=get_member_id(request))

        campaign_list=campaign.objects.get(campaign_id=campaign_id)

        return render(request,'services/export_group.html',{"group_model":group_model,'campaign_id':campaign_id})
    else: return HttpResponseRedirect('/index/')

def group_import_view(request,campaign_id,group_id):
    if request.session.get('login_session', False) == True:
        new_group=groups()
        import_group=groups.objects.get(group_id=group_id)

        #campaign_id=request.session.get['campaign_id']

        new_group.group_name=import_group.group_name
        new_group.campaign_id=campaign.objects.get(campaign_id=campaign_id)
        new_group.member_id=import_group.member_id
        new_group.group_description=import_group.group_description
        new_group.created_date=todays()

        new_group.save()
        return HttpResponseRedirect('/campaign/config/'+str(campaign_id)+'/')
    else: return HttpResponseRedirect('/index/')

def import_user_view(request,campaign_id):
    if request.session.get('login_session', False) == True:
        group_model=groups.objects.filter(member_id=get_member_id(request))
        campaign_list=campaign.objects.filter(member_id=get_member_id(request))


        return render(request,'services/groups.html',{"group_model":group_model,'campaign_list':campaign_list})
    else: return HttpResponseRedirect('/index/')

#user group logic-------------------------------------------------------------------------------------------------------------

def group_view(request): #display list of users
    if request.session.get('login_session', False) == True:
        group_model=groups.objects.filter(member_id=get_member_id(request))
        campaign_list=campaign.objects.filter(member_id=get_member_id(request))
        return render(request,'services/groups.html',{"group_model":group_model,'campaign_list':campaign_list})
    else: return HttpResponseRedirect('/index/')


def new_group_view(request,campaign_id=None):
    if request.session.get('login_session', False) == True:
        print('id',request.GET.get('campaign_id'))
        if campaign_id is None:
            return render(request, 'services/groups_new.html')
        else:
            campaign_name=campaign.objects.get(campaign_id=campaign_id)
            campaign_name=campaign_name.campaign_name
            return render(request,'services/groups_new.html',{'campaign_name':campaign_name})

    else: return HttpResponseRedirect('/index/')

def add_group_view(request):
    if request.session.get('login_session', False) == True:
        group_name= request.POST.get('group_name','')
        group_desc = request.POST.get('group_desc', '')
        campaign_name= request.POST.get('campaign_name', '')

        mem_id = request.session.get('user_id')  # users id stored session in login/auth view
        member_id=members.objects.get(id=mem_id)

        camp=campaign.objects.get(campaign_name=campaign_name,member_id=member_id)
        print(camp.campaign_id)

        #new_group=groups()

        if campaign=='':
            new_group=groups(group_name=group_name,group_description=group_desc,member_id=member_id)
        else:
            new_group = groups(group_name=group_name, group_description=group_desc,campaign_id=camp, member_id=member_id)

        new_group.save()

        return HttpResponseRedirect('campaign/config/'+str(camp.campaign_id)+'/')

    else: return HttpResponseRedirect('/index/')

def group_remove_view(request,group_id):

    if request.session.get('login_session', False) == True:
        camp = campaign.objects.get(group_id=group_id)
        camp.delete()
        return HttpResponseRedirect('/campaign/')
    return HttpResponseRedirect('/index/')
def group_detail_view(request,group_id):#dispays the detail view when u click details link in dashboard
    if request.session.get('login_session', False) == True:
        print()
    return HttpResponseRedirect('/index/')


#user logic-------------------------------------------------------------------------------------------------------------
def users_view(request): #display list of users
    if request.session.get('login_session', False) == True:
        #user_list=attack_users.objects.filter(member_id=get_member_id(request))
        mem_id = request.session.get('user_id')  # users id stored session in login/auth view
        member_id = members.objects.get(id=request.session.get('user_id'))
        user_list = userss.objects.filter(member_id=member_id)
        return render(request,'services/users.html',{'user_list':user_list})

    return HttpResponseRedirect('/index/')
def new_user_view(request,group_id=None):#display the page for adding new users
    if request.session.get('login_session', False) == True:
        group_model=groups.objects.filter(member_id=get_member_id(request))

        print(group_id)

        if group_id is None:
            print('we in if')
            return render(request, 'services/users_new.html',{"group_model": group_model,'hidden_txt':'hidden','hidden_select':''})
        else:
            print('we in else')
            g_name=groups.objects.get(group_id=group_id)
            return render(request,'services/users_new.html',{"group_model":group_model,'group_name':g_name.group_name,'hidden_txt':'','hidden_select':'hidden'})
    else: return HttpResponseRedirect('/index/')

def add_user_view(request):
    if request.session.get('login_session', False) == True:
        fname=request.POST.get('fname','')
        lname=request.POST.get('lname','')
        email=request.POST.get('email','')
        group_name=request.POST.get('group','')

        if group_name=='':
            new_user=userss(fullname=fname+' '+lname,useremail=email,member_id=get_member_id(request))
            new_user.save()
            return HttpResponseRedirect('/user/')
        else:
            mem_id = request.session.get('user_id')  # users id stored session in login/auth view
            member_id = members.objects.get(id=request.session.get('user_id'))

            group=groups.objects.get(group_name=group_name)
            idd=group.group_id

            #new_user=userss(fullname=fname+' '+lname,useremail=email,member_id=get_member_id(request),group_id=group_id.group_id)
            new_user = userss(fullname=fname + ' ' + lname, useremail=email, member_id=member_id,group_id=group)

            new_user.save()
            group_users=userss.objects.filter(group_id=group.group_id)
            return HttpResponseRedirect('/campaign/details/users/'+str(group.group_id),{"group_users":group_users})

    return HttpResponseRedirect('/index/')

def user_remove_view(request, group_id):
    if request.session.get('login_session', False) == True:
        camp = campaign.objects.get(group_id=group_id)
        camp.delete()
        return HttpResponseRedirect('/campaign/')

    return HttpResponseRedirect('/index/')




#landing page logic-------------------------------------------------------------------------------------------------------------
def landing_pages(request):

    if request.session.get('login_session', False) == True:
        page_list = landin_page.objects.filter(member_id=get_member_id(request))

        return render(request, 'services/landing_page.html', {'pages': page_list})
    else: return HttpResponseRedirect('/index/')

def new_page(request):

    if request.session.get('login_session', False) == True:
        return render(request, 'services/new_landing_page.html')
    else: return HttpResponseRedirect('/index/')


def add_landing_pages(request):
    if request.session.get('login_session', False) == True:
        page_name = request.POST.get('page_name', '')
        new_page = landin_page(page_name=page_name, page_upload=request.FILES.get('page_upload'))
        new_page.save()
    return HttpResponseRedirect('/langing/')  # file=request.POST.get('page_upload')
# from pprint import pprint
# pprint(request.POST)
# pprint(request.FILES)
# file = request.FILES['page_upload']

def landing_page_remove_view(request, group_id):
    if request.session.get('login_session', False) == True:
        camp = campaign.objects.get(group_id=group_id)
        camp.delete()
        return HttpResponseRedirect('/campaign/')

    return HttpResponseRedirect('/index/')

#email template logic---------------------------------------------------------------------------------------------------
def email_send(request):
    hello='hello'
    return render(request,'services/mail.html')
def email_sender(request):
    hello='hello'
    return render(request,'services/mail.html')
def email_sender(request):
    return render(request,'services/mailer.html')


#profile template logic----------------------------------------------------------------------------------------
def profile_view(request): #display list of users
    if request.session.get('login_session', False) == True:
        profiles=sending_profiles.objects.filter(member_id=get_member_id(request))
        return render(request, 'services/profile.html',{'profiles':profiles})
    else: return HttpResponseRedirect('/index/')

def new_profile(request):  # display list of users
        if request.session.get('login_session', False) == True:
            profile_name=request.POST.get('profile_name','')

            group_model = groups.objects.filter(member_id=get_member_id(request))
            return render(request, 'services/profile_new.html')
        else:
            return HttpResponseRedirect('/index/')

def add_profile(request): #display list of users
    if request.session.get('login_session', False) == True:
        profile_name = request.POST.get('profile_name', '')
        profile_email = request.POST.get('profile_email', '')
        profile_password = request.POST.get('profile_password', '')
        profile_server = request.POST.get('profile_server', '')
        profile_port = request.POST.get('profile_port', '')
        profile_header = request.POST.get('profile_from', '')

        mem_id = request.session.get('user_id')  # users id stored session in login/auth view
        member_id = members.objects.get(id=request.session.get('user_id'))

        profile = sending_profiles(profile_name=profile_name, profile_email=profile_email,
                                   profile_password=profile_password, profile_server=profile_server,
                                   profile_port=profile_port, profile_header=profile_header,
                                   member_id=member_id)
        msg=''
        if request.POST.get('btnsave'):
            profile.save()
            return HttpResponseRedirect('/profiles/',)
        if request.POST.get('btnsaveadd'):
            profile.save()
            return HttpResponseRedirect('/profiles/new/',{'msg':'The '+profile_name+' Profile has been added'})

    return HttpResponseRedirect('/index/')

def edit_profile_view(request,profile_id):
    profile=sending_profiles.objects.get(profile_id=profile_id)
    return  render(request,'services/profile_edit.html',{'profiles':profile})

def save_edit_profile_view(request):
    if request.session.get('login_session', False) == True:
        profile_name = request.POST.get('profile_name', '')
        profile_email = request.POST.get('profile_email', '')
        profile_password = request.POST.get('profile_password', '')
        profile_server = request.POST.get('profile_server', '')
        profile_port = request.POST.get('profile_port', '')
        profile_header = request.POST.get('profile_from', '')

        mem_id = request.session.get('user_id')  # users id stored session in login/auth view
        member_id = members.objects.get(id=request.session.get('user_id'))


        profile = sending_profiles(profile_name=profile_name, profile_email=profile_email,
                                   profile_password=profile_password, profile_server=profile_server,
                                   profile_port=profile_port, profile_header=profile_header,
                                   member_id=member_id)

        profile.save()
        return HttpResponseRedirect('/profiles/')
    return HttpResponseRedirect('/index/')

def profile_details_view(request):
    return render(request,'services/users.html')

def profile_remove_view(request, group_id):
    if request.session.get('login_session', False) == True:
        camp = campaign.objects.get(group_id=group_id)
        camp.delete()
        return HttpResponseRedirect('/campaign/')

    return HttpResponseRedirect('/index/')

def done_profile(request):
    return HttpResponseRedirect('/profiles/')

def see(request):
    myuser = groups.objects.select_related('campaign_id').filter(campaign_id=5)

    for usr in myuser:
        print(str(usr))
    return HttpResponseRedirect('/campaign/')


#My profile----------------------------------------------------------------------------------------------------
def user_profile(request):
    if request.session.get('login_session', False) == True:
        member=members.objects.get(id=get_member_id(request))
        return render(request, 'services/member_profile.html',{'member':member})
    return HttpResponseRedirect('/index/')

def save_user_profile(request):
    if request.session.get('login_session', False) == True:
        username = request.POST.get('username', '')
        first_name = request.POST.get('firstname', '')
        last_name = request.POST.get('surname', '')
        email = request.POST.get('email', '')
        organization = request.POST.get('organization', '')

        member = members.objects.get(id=get_member_id(request))
        member.username=username
        member.first_name=first_name
        member.last_name=last_name
        member.email=email
        member.organization=organization

        member.save()

        return  HttpResponseRedirect('/userprofile/')


    return HttpResponseRedirect('/index/')