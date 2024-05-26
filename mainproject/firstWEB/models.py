from django.db import models

# Create your models here.
#一個Class 一張表的描述
class cal(models.Model):
    value_a =models.CharField(max_length=10)
    value_b =models.CharField(max_length=10)
    result =models.CharField(max_length=10)

class Dialogue(models.Model):
    user_id = models.CharField(max_length=50)
    file_name = models.CharField(max_length=100)

    def __str__(self):
        return f"User ID: {self.user_id}, File Name: {self.file_name}"
    


class Doctor(models.Model):
    idNumber = models.CharField(max_length=20, unique=True, null=False)
    name = models.CharField(max_length=100, null=False)
    department = models.CharField(max_length=100, null=False)
    sex = models.CharField(max_length=2, default='M', null=False)
    hire_date = models.DateField(null=False)
    resign_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
    ]

    idNumber = models.CharField(max_length=20, unique=True, verbose_name="身分證字號")
    name = models.CharField(max_length=100, verbose_name="姓名")
    phone = models.CharField(max_length=50, verbose_name="電話")
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="性別")
    birthday = models.DateField(verbose_name="生日")
    allergens = models.CharField(max_length=255, verbose_name="過敏物")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "病患"
        verbose_name_plural = "病患"

    
    

