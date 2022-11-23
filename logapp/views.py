from ast import Delete
from functools import partial
from itertools import count
import json
from logging import exception
from tkinter import EXCEPTION
import traceback
from turtle import color
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from logapp.models import Question, Userdata
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from logapp.serilizer import Userdataserializer
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
def addd(request):
    a=Userdata.objects.filter(password__in=[4444444,9999999])

    
    return render(request,"orm.html",{"a":a})
    
@api_view(['POST'])
def addUser(request):
    print(request.data)
    userFromClient=request.data # JSON String received from client will be converted into dictionary object . It is done by API internally .
    Userdata.objects.create(username=userFromClient["username"],password=userFromClient["password"],mobile_no=userFromClient["mobile_no"])
    response=Response({"message":"object added in database"})
    response['Access-Control-Allow-Origin']="http://localhost:4200";
    return response
@api_view(['POST'])
def log(request):
    userfromclient=request.data
    try:
        usersfromdb=Userdata.objects.get(username=userfromclient["username"])
    
        if usersfromdb.username==userfromclient["username"] and usersfromdb.password==userfromclient["password"]:
            response=Response({"login"})
        
            return response
    except Userdata.DoesNotExist:
        userfromdb=None 
        response=Response({"not exit"})
        return response
        

    
@api_view(['PUT'])
def userUpdate(request):
    userfromclient=request.data
    usersfromdb=Userdata.objects.get(username=userfromclient["username"])
    usersfromdb.password=userfromclient["password"]
    usersfromdb.mobile_no=userfromclient["mobile_no"]
    usersfromdb.save()
    response=Response({"data updated"})
    response['Access-Control-Allow-Origin']="http://localhost:4200"
    return response

@api_view(['DELETE'])
def userDelete(request,username):
    Userdata.objects.filter(username=username).delete()
    response=Response({"data deleted"})
    response['Access-Control-Allow-Origin']="http://localhost:4200"
    return response

@api_view(["GET"])
def getuser(request,username):
    username=Userdata.objects.get(username=username)
    response=Response({"username":username.username,"password":username.password,"mobile_no":username.mobile_no})
    response['Access-Control-Allow-Origin']="http://localhost:4200"
    return response


@api_view(['GET'])

def getalluser(request):
    user=Userdata.objects.all()
    all_list=[]
    for i in user:
        all_list.append({"username":i.username,"password":i.password,"mobile_no":i.mobile_no})
    
    
    response=Response(all_list)
    response['Access-Control-Allow-Origin']="http://localhost:4200";
    return response

def homepage(request):

    return render(request,'login.html')


def login(request):

    uname=request.GET['uname']
    upass=request.GET['upass']
    subject=request.GET['subject']

    if uname=='admin' and upass=='admin123':
        return render(request,'question.html',{'msg':"welcome admin"})
   
   
    formdb=Userdata.objects.get(username=uname)
    if uname==formdb.username and upass==formdb.password:

        request.session['uname']=uname
        request.session['upass']=upass
        request.session['ans']={}
        request.session['qno']=-1
        request.session['score']=0
        request.session['duration']=180

        return render(request,'welcome.html',{'subject':subject})
    else:
        return render(request,'login.html',{'res':"username and password incoorect"})

def showregister(request):
    return render(request,"register.html")


def register(request):
    username=request.GET['uname1']
    password=request.GET['upass1']
    mobile_no=request.GET['mobno1']
    
    Userdata.objects.create(username=username,password=password,mobile_no=mobile_no)
    return render(request,'login.html',{'msg':'resister successfully'})

def ajax(request):
    print(request.GET['sam'])
    msg='username already present'
    try:
        userdata=Userdata.objects.get(username=request.GET['sam'])
        print(userdata)
    except:
        msg='user does not exit.'


    data={"msg":msg}

    json_data=json.dumps(data)
    print("json string is ",json_data)

    response=HttpResponse(f'{json_data}',content_type='application/json')
    return response

def add(request):
    subject=request.GET['subject']
    qno=request.GET['qno']
    question=request.GET['qtext']
    A=request.GET['A']
    B=request.GET['B']
    C=request.GET['C']
    D=request.GET['D']
    ans=request.GET['ans']

    Question.objects.create(qno=qno,question=question,A=A,B=B,C=C,D=D,subject=subject,ans=ans)
    print("database saved")
    return render(request,'question.html',{'ms':'Data saved'})

def update(request):

    subject=request.GET['subject']
    qno=request.GET['qno']

    a=Question.objects.filter(qno=qno,subject=subject)
    a.update( question=request.GET['qtext'],
    A=request.GET['A'],
    B=request.GET['B'],
    C=request.GET['C'],
    D=request.GET['D'],
    ans=request.GET['ans'])

    return render(request,'question.html',{'ms':'Data udated'})

def delete(request):
    subject=request.GET['subject']
    qno=request.GET['qno']

    Question.objects.filter(qno=qno,subject=subject).delete()
   

    return render(request,'question.html',{'ms':'Data deleted'})

def views(request):
    print(request.GET['subject'])
    print(request.GET['qno'])

    
    a=Question.objects.get(subject=request.GET['subject'],qno=request.GET['qno'])
    print(a.question)

    data={
        'qtext':a.question,
        'A':a.A, 
        'B':a.B,
        'C':a.C,
        'D':a.D,
        'ans':a.ans
        }

    json_data=json.dumps(data)
    print(json_data)
    response=HttpResponse(f'{json_data}',content_type='application/json')
    return response

def this(request):
    t=Question.objects.get(qno=request.GET['qno'],subject=request.GET['subject'])

    return render(request,"question.html",{'t':t})

def next(request):
    try:
        subject=request.GET['subject']
        questions=Question.objects.filter(subject=subject)
        print(questions)
        request.session['qno']=request.session['qno']+1
        b=questions[request.session['qno']]
        a=b.qno
        all=request.session['ans']
        don=''
        for i,j in all.items():
            if int(i)==a:
                don=j[2]
        print(don)
        return render(request,'welcome.html',{'don':don,'qno':b.qno,'qtext':b.question,'A':b.A,'B':b.B,'C':b.C,'D':b.D,'ans':b.ans,'subject':subject})


    except:
        print(subject)
        request.session['qno']=0
        b=questions[request.session['qno']]
        a=b.qno
        all=request.session['ans']
        don=''
        for i,j in all.items():
            if int(i)==a:
                don=j[2]
        print(don)
        return render(request,'welcome.html',{'don':don,'qno':b.qno,'qtext':b.question,'A':b.A,'B':b.B,'C':b.C,'D':b.D,'ans':b.ans,'subject':subject})


def previous(request):
    try:
        subject=request.GET['subject']
        questions=Question.objects.filter(subject=subject)
        print(questions)
        request.session['qno']=request.session['qno']-1
        b=questions[request.session['qno']]
        a=b.qno
        all=request.session['ans']
        don=''
        for i,j in all.items():
            if int(i)==a:
                don=j[2]
        print(don)
        return render(request,'welcome.html',{'don':don,'qno':b.qno,'qtext':b.question,'A':b.A,'B':b.B,'C':b.C,'D':b.D,'ans':b.ans,'subject':subject})

    except:
        request.session['qno']=1
        b=questions[request.session['qno']]
        a=b.qno
        all=request.session['ans']
        don=''
        for i,j in all.items():
            if int(i)==a:
                don=j[2]
        print(don)
        return render(request,'welcome.html',{'don':don,'qno':b.qno,'qtext':b.question,'A':b.A,'B':b.B,'C':b.C,'D':b.D,'ans':b.ans,'subject':subject})

def currentans(request):
    a=request.session['ans']
    a[request.GET['qno']]=list([request.GET['qtext'],request.GET['ans'],request.GET['op'],request.GET['qno']])
    request.session['ans']=a
    
    return render(request,'welcome.html')

def cal(request):
    try:
        a=request.session['ans']
        result=a.values()
        for i in result:
            if i[1]==i[2]:
                request.session['score']=request.session['score']+1
        finalscore=request.session['score']
        print(type(finalscore))
        if finalscore<=5:
            msg="Fail"
        else:
            msg="Pass"
        del request.session['ans']
        del request.session['score']
    except Exception as msg:
        return render(request,'login.html')

    return render(request,'score.html',{'finalscore':finalscore,'result':result,'msg':msg})

def showtime(request):
    request.session['duration']=request.session['duration']-1
    return HttpResponse(request.session['duration'])


@api_view(['GET'])
def getuser1(request,username):
    userfromdb=Userdata.objects.get(username=username)
    serializer=Userdataserializer(userfromdb)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
#@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])

def getalluser1(request):
    userfromdb=Userdata.objects.all()
    serializer=Userdataserializer(userfromdb,many=True)
    return Response(serializer.data)

@api_view(['POST'])

def adduser1(request):
    serializer=Userdataserializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    #user=Userdata.objects.get(username=serializer.data['username'])
    #refresh=RefreshToken.for_user(user)
        
    return Response(serializer.data)#{'refresh':str(refresh),"access":str(refresh.access_token)})

@api_view(['PUT'])
def updateuser1(request):
    userfromclient=request.data
    userfromdb=Userdata.objects.get(username=userfromclient['username'])
    serializer=Userdataserializer(userfromdb,data=userfromclient,partial=False)
    if serializer.is_valid():
        serializer.save()
    return Response("data updated")


from django.views import View
class Abc(View):
    def get(self,request):
        return HttpResponse("<h1> this is get method <\h1>")

    def post(self,request):
        return HttpResponse("<h1> this is post method <\h1>")
class Acb(View):
    def get(self,request):
        name=request.GET['que']
        if name=='next':
            return HttpResponse("<h1> this get in one next </h1>")
        else:
            return HttpResponse("<h1> this post in one previous </h1>")
