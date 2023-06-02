from flask import Flask, render_template
import requests
import tkinter as tk 
from tkinter import ttk

app = Flask(__name__)  # instance of flask app with name app

def hello():
    print(" Successfully entered details ")


root = tk.Tk()
root.title(" Enter Details ")

url = tk.StringVar()
username = tk.StringVar()
password = tk.StringVar()

url_label = ttk.Label(root, text= "Enter Jenkins URL : ")
url_label.pack(side="left")
url_entry = ttk.Entry(root, textvariable=url)
url_entry.pack(side='left')


username_label = ttk.Label(root, text= "Enter Jenkins username : ")
username_label.pack(side="left")
username_entry = ttk.Entry(root, textvariable=username)
username_entry.pack(side='left')

password_label = ttk.Label(root, text= "Enter token : ")
password_label.pack(side="left")
password_entry = ttk.Entry(root, textvariable=password)
password_entry.pack(side='left')


submit_button = ttk.Button(root, text="Submit", command=hello)
submit_button.pack(side="left", padx=(0,10))

quit_button = ttk.Button(root, text="quit", command=root.quit)
quit_button.pack(side="left")


root.mainloop()

url2 = url.get()
username2 = username.get()
password2 = password.get()

url2 = url2 + 'api/json'
print(f"url2 == {url2}")
print(f"username2 == {username2}")
print(f"password2 == {password2}")


response = requests.get(url2, auth=(username2, password2))
print("response")

headers2 = response.headers



print(response.json()['jobs'])

# Jenkins 2
count2 = 0
job_list2 = response.json()['jobs']   # List of dictionaries 
print(job_list2)
for job in job_list2:
    print(f"job ===== {job}")
    count2 += 1
    print(f"job url == {job['url']}")
    
    ur = job['url'] + 'api/json'
    res1 = requests.get(ur, auth=(username2, password2))
    print(res1.content.decode)
    print(res1.json()['name'])
    print(res1.json()['url'])  
    
  
    urllsb2 = job['url'] + 'lastSuccessfulBuild/api/json'
    res2 = requests.get(urllsb2, auth=(username2, password2))
    
    job['lastSuccessfulBuildnum'] = res2.json()['number'] # last success
    job['lastSuccessfulBuildqid'] = res2.json()['queueId'] # last success
    job['lastSuccessfulBuilddur'] = res2.json()['duration'] # last success
    job['lastSuccessfulBuildurl'] = res2.json()['url'] # last success
    job['lastSuccessfulBuildresult'] = res2.json()['result'] # last success
    
    urllb = job['url'] + 'lastBuild/api/json'
    res4 = requests.get(urllb,auth=(username2,password2))
    job['lastBuildResult'] = res4.json()['result']
    
    res3 = requests.get(ur, auth=(username2, password2))
    if res3.json()['lastFailedBuild'] is None:
        job['lastFailedBuildNum'] = "Null"
    else:
        job['lastFailedBuildNum'] = res3.json()['lastFailedBuild']['number']

urlv = 'https://updates.jenkins.io/update-center.actual.json'
response5 = requests.get(urlv)
ver = response5.json()['core']['version']

headers2['X-Jenkins'] = '2.397'
if headers2['X-Jenkins'] < ver:
    cmpb = ' Not up to date'
else:
    cmpb = ' Up to date '
    
@app.route("/")                               # when user enters the root URL home function is executed
def home():
    
    if response.status_code == 200:
    
       return render_template('jenkins.html', jobs2=job_list2,count2=count2,headers2=headers2,ver=ver,cmpb=cmpb )


# @app.route('/submit-form', methods=['POST'])
# def submit_form():
#     name = requests.form['name']
#     email = requests.form['email']
#     return render_template('jenkins.html',username=name,email=email)
