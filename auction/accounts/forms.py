from django import forms
from app.models import Customer

class Registration(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'special', 'size': 50}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'special', 'size': 50}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'special', 'size': 50}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'special', 'size': 50}))

    class Meta:
        model = Customer
        fields = ['username', 'address', 'password', 'confirm_password']

    def clean(self):
        super().clean()
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Password are different...Check it!')
        return self.cleaned_data