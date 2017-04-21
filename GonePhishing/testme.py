import smtplib
import email.utils
from email.mime.text import MIMEText


import hashlib,random, string

mychars = ''
for i in range(16):
    mychars = mychars + random.choice(string.ascii_letters)
print(mychars)

phish_url='http://127.0.0.1:8000/gophish/hooked/'+mychars+'/'
print(phish_url)
"""letter=random.choice(string.ascii_letters) +""+random.choice(string.ascii_letters)+random.choice(string.ascii_letters) +""+random.choice(string.ascii_letters)

md5letter=hashlib.md5(letter.encode('utf-8')).hexdigest()
print(letter)
print(md5letter)"""
#random_id = random.randint(1, 1000)  # generate random id
#hash_id = hashlib.md5(repr(random_id).encode('utf-8')).hexdigest()

#print(hash_id)
""""
def write_urls(data):
    file=open("C:\\Users\\Joe\\Documents\\test.txt","a+")
    for item in data:
        file.write(item+ "\n")
    file.close()

datlist=["a","b","c","e"]

write_urls(datlist)"""
"""def add_str_to_lines(f_name, str_to_add):
    with open(f_name, "r") as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            lines[index] = line.strip() + str_to_add + "\n"

    with open(f_name, "w") as f:
        for line in lines:
            f.write(line)

if __name__ == "__main__":
    str_to_add = " foo"
    f_name = "C:\\Users\\Joe\\Documents\\test.txt","a+"
    add_str_to_lines(f_name=f_name, str_to_add=str_to_add)

    with open(f_name, "r") as f:
        print(f.read())
def test(request):
    request.session['login_session']=False
    print(request.session['login_session'])

    del request.session['login_session']
    print(request.session['login_session'])



test('GET')"""

#victims_model = models.victims.objects.all()  # get victims list

#for vic in victims_model:
 #   if vic.auto_id=
#numbers=[1,2,3,4,5,6]



""""print (random_id)
def genereate_id(number):
    for num in numbers:
    #for victim in victims_model:
        random_id=0
        if num == number:
            random_id = random.randint(1, 100)
            genereate_id(random_id)
        else:
            random_id = number
            return random_id

print (genereate_id(random_id))"""
"""print (random.randint(1,100))
username='alex el grande'
victim='aramantswana@csir.co.za'

# Create the message
msg = MIMEText('Hello '+ username+' click on the link below to collect your million bucks\n\n "https://127.0.0.1/8000/bitedust/1/  to Claim Prize Now\n before its too late"')
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
    server.quit()"""

