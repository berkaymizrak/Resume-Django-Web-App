from django import forms

from .models import *


class ContactForm(forms.Form):
    name = forms.CharField(
        required=True,
        max_length=Message._meta.get_field('name').max_length,
        label=Message._meta.get_field('name').verbose_name,
        help_text=Message._meta.get_field('name').help_text,
        widget=forms.TextInput(attrs={
            'placeholder': '',
            'type': 'text',
        }),
    )
    email = forms.EmailField(
        required=True,
        max_length=Message._meta.get_field('email').max_length,
        label=Message._meta.get_field('email').verbose_name,
        help_text=Message._meta.get_field('email').help_text,
        widget=forms.TextInput(attrs={
            'placeholder': 'ex@domain.com',
            'type': 'text',
        }),
    )
    message = forms.CharField(
        required=True,
        max_length=Message._meta.get_field('message').max_length,
        label=Message._meta.get_field('message').verbose_name,
        help_text=Message._meta.get_field('message').help_text,
        widget=forms.Textarea(attrs={
            'placeholder': 'Message...',
            'type': 'text',
            # 'rows': 4,
            # 'cols': 80,
        }),
    )


