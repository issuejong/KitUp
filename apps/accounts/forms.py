from django import forms
from .models import User, TechStack


class OnboardingForm(forms.ModelForm):
    tech_stacks = forms.ModelMultipleChoiceField(
        queryset=TechStack.objects.all().order_by("category", "name"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="기술 스택 (선택)",
        help_text="보유한 기술을 선택하세요",
    )

    class Meta:
        model = User
        fields = ["nickname", "github_id", "profile_image", "tech_stacks"]
        widgets = {
            "nickname": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "닉네임을 입력하세요",
            }),
            "github_id": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "GitHub 아이디 (선택)",
            }),
            "profile_image": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["tech_stacks"].initial = self.instance.tech_stacks.all()

    def clean_nickname(self):
        nick = (self.cleaned_data.get("nickname") or "").strip()
        if not nick:
            raise forms.ValidationError("닉네임은 필수입니다.")
        if User.objects.filter(nickname=nick).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("이미 사용 중인 닉네임입니다.")
        return nick

    def clean_github_id(self):
        github_id = (self.cleaned_data.get("github_id") or "").strip()
        if github_id and User.objects.filter(github_id=github_id).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("이미 등록된 GitHub 아이디입니다.")
        return github_id or None

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            user.tech_stacks.set(self.cleaned_data.get("tech_stacks", []))
        return user


class ProfileUpdateForm(forms.ModelForm):
    tech_stacks = forms.ModelMultipleChoiceField(
        queryset=TechStack.objects.all().order_by("category", "name"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="기술 스택 (선택)",
        help_text="보유한 기술을 선택하세요",
    )

    class Meta:
        model = User
        fields = ["nickname", "github_id", "profile_image", "bio", "tech_stacks"]
        widgets = {
            "nickname": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "닉네임을 입력하세요",
            }),
            "github_id": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "GitHub 아이디 (선택)",
            }),
            "profile_image": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
            }),
            "bio": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "자기소개를 입력하세요",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["tech_stacks"].initial = self.instance.tech_stacks.all()

    def clean_nickname(self):
        nick = (self.cleaned_data.get("nickname") or "").strip()
        if not nick:
            raise forms.ValidationError("닉네임은 필수입니다.")
        if User.objects.filter(nickname=nick).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("이미 사용 중인 닉네임입니다.")
        return nick

    def clean_github_id(self):
        github_id = (self.cleaned_data.get("github_id") or "").strip()
        if github_id and User.objects.filter(github_id=github_id).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("이미 등록된 GitHub 아이디입니다.")
        return github_id or None

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            user.tech_stacks.set(self.cleaned_data.get("tech_stacks", []))
        return user
