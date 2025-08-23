import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import AllowedMatric, Profile

User = get_user_model()

def normalize_matric(value: str) -> str:
    """
    Normalize user-typed matric numbers:
    - strip leading/trailing whitespace
    - collapse internal whitespace
    - keep only digits (adjust if your format includes letters)
    """
    if not value:
        return ""
    # remove spaces and tabs entirely
    v = re.sub(r"\s+", "", value.strip())
    return v

class SignupForm(UserCreationForm):
    full_name = forms.CharField(
        label="Full name", max_length=200, required=True,
        widget=forms.TextInput(attrs={"placeholder": "Full name"})
    )
    matric_number = forms.CharField(
        label="Matric number", max_length=50, required=True,
        widget=forms.TextInput(attrs={"placeholder": "Matric number"})
    )
    department = forms.CharField(
        label="Department", max_length=50, required=True,
        widget=forms.TextInput(attrs={"placeholder": "Department"})
    )
    serial_number = forms.CharField(
        label="Serial number", max_length=100, required=True,
        widget=forms.TextInput(attrs={"placeholder": "Serial number"})
    )
    newsletter = forms.BooleanField(
        label="Receive Weekly Emails", required=False, initial=False
    )
    username = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    # --- Temporary hardcoded whitelist (edit here while the freeze is active) ---
    TEMP_ALLOWED = [
        "20221351185",
        "20223453434",
        "20224567890",
        "20221234567",
    ]
    # ---------------------------------------------------------------------------

    def clean_matric_number(self):
        raw = self.cleaned_data.get("matric_number")
        matric = normalize_matric(raw)

        if not matric:
            raise forms.ValidationError("Matric number is required.")

        # 1) Temporary gate: must be in hardcoded list
        if matric not in self.TEMP_ALLOWED:
            raise forms.ValidationError("This matric number is not currently allowed for signup.")

        # 2) DB allowlist gate
        try:
            allowed = AllowedMatric.objects.get(matric_number=matric)
        except AllowedMatric.DoesNotExist:
            raise forms.ValidationError("This matric number is not authorized (not found in allowlist).")

        if allowed.used:
            raise forms.ValidationError("You have already signed up with this matric number! Try login in.")

        # Store normalized version so save() uses it
        self.cleaned_data["matric_number"] = matric
        return matric

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Passwords do not match.")
        return cleaned

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        matric = self.cleaned_data.get("matric_number")

        # Use matric as username
        if not user.username:
            user.username = matric

        user.email = self.cleaned_data.get("email", "")
        full_name = self.cleaned_data.get("full_name", "")
        parts = full_name.strip().split(None, 1)
        if parts:
            user.first_name = parts[0]
            if len(parts) > 1:
                user.last_name = parts[1]

        if commit:
            user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.matric_number = matric
            profile.serial_number = self.cleaned_data.get("serial_number", "")
            profile.department = self.cleaned_data.get("department", "")
            profile.newsletter = bool(self.cleaned_data.get("newsletter", False))
            profile.save()

            # Mark matric as used (inside the same transaction)
            AllowedMatric.objects.filter(matric_number=matric, used=False).update(used=True)

        return user

class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(max_length=200, required=True, label="Full name")

    class Meta:
        model = Profile
        fields = ["matric_number", "serial_number", "department", "newsletter", "avatar"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["full_name"].initial = f"{user.first_name} {user.last_name}"
            self.fields["email"] = forms.EmailField(initial=user.email, required=True)
        self.fields["matric_number"].disabled = True
        self.fields["serial_number"].disabled = True
        self.fields["email"].disabled = True
        self.fields["department"].disabled = True

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        full_name = self.cleaned_data.get("full_name", "").split(None, 1)
        user.first_name = full_name[0]
        if len(full_name) > 1:
            user.last_name = full_name[1]
        user.email = self.cleaned_data.get("email", user.email)
        if commit:
            user.save()
            profile.save()
        return profile   
