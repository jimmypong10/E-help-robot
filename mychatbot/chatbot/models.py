from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'
    
class PatientRecord(models.Model):
    identifier = models.CharField(max_length=100)  # 身分證號
    patient_id = models.CharField(max_length=100)  # 病患編號

    def __str__(self):
        return f"ID: {self.identifier}, Patient ID: {self.patient_id}"

class PatientRecord_Detail(models.Model):
    identifier = models.CharField(max_length=50)  # 身分證號
    patient_id = models.CharField(max_length=50)  # 病患編號
    date = models.DateField()  # 診斷日期
    doctor_id = models.CharField(max_length=50)  # 醫生編號
    diagnosis = models.TextField()  # 診斷內容

    class Meta:
        unique_together = ('patient_id', 'date', 'doctor_id', 'diagnosis')

    def __str__(self):
        return f"Patient {self.identifier} - Record {self.patient_id}"
class Chat2(models.Model):  #聊天機器人用
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    image = models.ImageField(upload_to='images/save/',name='image',default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Chat3(models.Model):  #聊天機器人3用
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'
class picsave(models.Model): #圖片下載
    image = models.ImageField(upload_to='images/botinput/',name='image')