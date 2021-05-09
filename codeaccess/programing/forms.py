from .models import Profile
from django.forms import ModelForm
from django import forms


class ProfileEdit(ModelForm):
    """profile editing form .."""

    class Meta:
        """meta class.."""

        model = Profile

        fields = {'name', 'collegename', 'roll_no', 'about', 'course', 'branch'}

        widgets = {"name": forms.TextInput(attrs={'placeholder': "name", 'class': "form-label-group form-control "}),
                   "collegename": forms.TextInput(attrs={'placeholder': "name", 'class': "form-label-group form-control "}),
                   "roll_no": forms.TextInput(attrs={'placeholder': "roll_no", 'class': "form-label-group form-control "}),
                   "roll_no": forms.TextInput(attrs={'placeholder': "roll_no", 'class': "form-label-group form-control "}),
                   # "about": forms.TextInput(attrs={'placeholder': "about", 'class': "form-label-group form-control "}),
                   "course": forms.TextInput(attrs={'placeholder': "course", 'class': "form-label-group form-control "}),
                   "branch": forms.TextInput(attrs={'placeholder': "branch", 'class': "form-label-group form-control "}),

                   }
        labels = {"name": "Name",
                  "collegename": "collegename",
                  "roll_no": 'roll_no',
                  "about": "about",
                  "course": "course",
                  "branch": "branch",
                  }
        ordering = {"name", "collegename", 'roll_no', "about", "course", "branch"}


class UpdateProfileImg(ModelForm):
    """docstring for ClassName..."""

    class Meta:
        """meta class.."""
        model = Profile
        fields = {'image',}


        

