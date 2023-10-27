
from django.forms import ModelForm
from accounts.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "phone_number", "password"]
    
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user