from django import forms
from .models import ContactUsForm

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUsForm
        fields = ['email', 'subject', 'message']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control mb-3', 'placeholder': 'ایمیل معتبر'}),
            'subject': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'موضوع پیام'}),
            'message': forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': 'متن پیام', 'rows': 9}),
        }
        labels = {
            'email': 'ایمیل',
            'subject': 'موضوع پیام',
            'message': 'متن پیام',
        }