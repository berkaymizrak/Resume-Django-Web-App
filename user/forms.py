from django import forms

from user import models


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


class SkillAdminForm(forms.ModelForm):
    percent = forms.CharField(
        widget=forms.NumberInput(attrs={"type": "range", "min": 0, "max": 100}),
        label=models.Skill._meta.get_field('percent').verbose_name,
    )

    class Meta:
        model = models.Skill
        fields = "__all__"

