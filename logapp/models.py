
from django.db import models
from django.forms import CharField
from platformdirs import user_data_path

class Userdata(models.Model):
    username=models.CharField(max_length=20,primary_key=True)
    password=models.CharField(max_length=20)
    mobile_no=models.IntegerField()



    def __str__(self):
        return "{},{},{}".format(self.username,self.password,self.mobile_no)

    class Meta:
        db_table='userdata'

class Question(models.Model):
    qno=models.IntegerField(primary_key=True)
    question=models.CharField(max_length=60)
    A=models.CharField(max_length=10)
    B=models.CharField(max_length=10)
    C=models.CharField(max_length=10)
    D=models.CharField(max_length=10)
    subject=models.CharField(max_length=20)
    ans=models.CharField(max_length=20)
    
    def __str__(self):
        return "{},{},{},{},{},{},{},{}".format(self.qno,self.question,self.A,self.B,self.C,self.D,self.subject,self.ans)

    class Meta:
        db_table='question'