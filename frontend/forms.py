from django import forms
from frontend import models


class SkillAdminForm(forms.ModelForm):
    percent = forms.CharField(
        widget=forms.NumberInput(attrs={"type": "range", "min": 0, "max": 100}),
        label=models.Skill._meta.get_field('percent').verbose_name,
    )

    class Meta:
        model = models.Skill
        fields = "__all__"
