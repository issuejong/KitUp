from django import forms
from .models import User

class OnboardingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["nickname", "profile_image"]

    def clean_nickname(self):
        nick = (self.cleaned_data.get("nickname") or "").strip()
        if not nick:
            raise forms.ValidationError("닉네임은 필수입니다.")
        if User.objects.filter(nickname=nick).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("이미 사용 중인 닉네임입니다.")
        return nick
