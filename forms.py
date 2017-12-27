from django import forms
from django.contrib.auth import (
                      authenticate,
                      get_user_model,
                      login,
                      logout,
                      )
                      
user = get_user_model()                      
                      

class UserLoginForm(forms.Form):
       username = forms.CharField()
       password = forms.CharField(widget=forms.PasswordInput)
       
       def clean_login(self, *args, **kwargs):
           username = self.cleaned_data.get('username')
           password = self.cleaned_data.get('password')
           
           user = authenticate(username=username, password=password)
           user_qs = user.objects.filter(username=username)
           if user_qs.count()== 1:
               user = user_qs.first()
           if not user:
              raise forms.ValidationError("this user does not exist")
           if not user.check_password(password):
               raise forms.ValidationError("Incorrect password")
               
           if not user.is_active:
                raise forms.ValidationError("this user no longer exist")
                
           return super(UserLoginForm, self).clean(*args, **kwargs)    
            
class UserRegisterForm(forms.ModelForm): 
       email = forms.EmailField(label='Email address')
       email2 = forms.EmailField(label='Confirm Email address')
       password = forms.CharField(widget=forms.PasswordInput)
       class Meta:
             model = user
             fields = ['username', 'email', 'email2', 'password']
             
             def clean_email(self, *args, **kwargs):
                email = self.cleaned_data.get('email')
                email2 = self.cleaned_data.get('email2')
                if email is email2:
                    raise forms.ValidationError("emails must match")
                email_qs = user.objects.filter(email=email)
                if email_qs.exists():
                        raise forms.ValidationError("this email has alreday registered")               
                 
                return super(UserRegisterForm,self).clean(*args, **kwargs)              
                 
              
