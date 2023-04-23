from django import forms
from core import models
from core import utils


class ContactForm(forms.Form):
    name = forms.CharField(
        required=True,
        max_length=models.Message._meta.get_field('name').max_length,
        label=models.Message._meta.get_field('name').verbose_name,
        help_text=models.Message._meta.get_field('name').help_text,
        widget=forms.TextInput(attrs={
            'placeholder': '',
            'type': 'text',
        }),
    )
    email = forms.EmailField(
        required=True,
        max_length=models.Message._meta.get_field('email').max_length,
        label=models.Message._meta.get_field('email').verbose_name,
        help_text=models.Message._meta.get_field('email').help_text,
        widget=forms.TextInput(attrs={
            'placeholder': 'ex@domain.com',
            'type': 'text',
        }),
    )
    subject = forms.CharField(
        required=True,
        max_length=models.Message._meta.get_field('subject').max_length,
        label=models.Message._meta.get_field('subject').verbose_name,
        help_text=models.Message._meta.get_field('subject').help_text,
        widget=forms.TextInput(attrs={
            'placeholder': '',
            'type': 'text',
        }),
    )
    message = forms.CharField(
        required=True,
        max_length=models.Message._meta.get_field('message').max_length,
        label=models.Message._meta.get_field('message').verbose_name,
        help_text=models.Message._meta.get_field('message').help_text,
        widget=forms.Textarea(attrs={
            'placeholder': 'Message...',
            'type': 'text',
            # 'rows': 4,
            # 'cols': 80,
        }),
    )

    def send_mail(self):
        if self.is_valid():
            name = self.cleaned_data['name']
            email = self.cleaned_data['email']
            subject = self.cleaned_data['subject']
            message = self.cleaned_data['message']
            message_context = 'Message received.\n\n' \
                              'Name: %s\n' \
                              'Subject: %s\n' \
                              'Email: %s\n' \
                              'Message: %s' % (name, subject, email, message)

            utils.send_mail_both(
                name=name,
                subject_mail='Message Received',
                subject_user=subject,
                message=message_context,
                to=email,
            )
            context = {
                'success': True,
                'message': '',
            }
        else:
            context = {
                'success': False,
                'message': 'Please fill all required fields.',
            }
        return context
