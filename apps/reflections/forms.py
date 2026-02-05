# reflections/forms.py
from django import forms
from .models import Retrospective

class RetrospectiveForm(forms.ModelForm):
    class Meta:
        model = Retrospective
        fields = ["project", "title", "content_md", "bookmarked"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "제목"}),
            "content_md": forms.Textarea(attrs={"rows": 16, "placeholder": "마크다운으로 작성하세요"}),
        }
