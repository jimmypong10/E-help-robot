from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Doctor,Patient
class DialogueForm(forms.Form):
    user_input = forms.CharField(label='', max_length=100)



class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="身分證字號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')    

class DoctorForm(forms.ModelForm):


    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
    ]

    department = forms.ChoiceField(label="科別", choices=[])
    sex = forms.ChoiceField(label="性別", choices=GENDER_CHOICES, widget=forms.RadioSelect)
    hire_date = forms.DateField(label="入職時間", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    resign_date = forms.DateField(label="離職時間", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    
    class Meta:
        model = Doctor
        fields = ['idNumber', 'name', 'department', 'sex', 'hire_date', 'resign_date']
        labels = {
            'idNumber': '身分證字號',
            'name': '名字',
            'hire_date': '入職時間',
            'resign_date': '離職時間'
        }
        widgets = {
            'idNumber': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control'}),
            'resign_date': forms.DateInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        departments = ['小兒科', '骨科']  # 在此添加您的科別選項
        self.fields['department'].choices = [(department, department) for department in departments]

class PatientForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
    ]

    idNumber = forms.CharField(label="身分證字號", max_length=20)
    name = forms.CharField(label="姓名", max_length=100)
    phone = forms.CharField(label="電話", max_length=50)
    sex = forms.ChoiceField(label="性別", choices=GENDER_CHOICES, widget=forms.RadioSelect)
    birthday = forms.DateField(label="生日", widget=forms.DateInput(attrs={'type': 'date'}))
    allergens = forms.CharField(label="過敏物", max_length=255)

    class Meta:
        model = Patient
        fields = ['idNumber', 'name', 'phone', 'sex', 'birthday', 'allergens']
        labels = {
            'idNumber': '身分證字號',
            'name': '姓名',
            'phone': '電話',
            'sex': '性別',
            'birthday': '生日',
            'allergens': '過敏物'
        }
        widgets = {
            'idNumber': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }