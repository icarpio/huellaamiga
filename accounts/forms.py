from django import forms
from django.contrib.auth import get_user_model

class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        help_text="Minimum 8 characters, must include letters and numbers."
    )
    password2 = forms.CharField(
        label="Confirma Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        help_text="Repeat the password to confirm."
    )
    is_protector = forms.BooleanField(
        required=False,
        label="Soy protectora/asociación"
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2', 'is_protector']


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields must match.")
        return password2

    def save(self, commit=True):
        # Guarda el usuario sin la contraseña, ya que la vamos a manejar manualmente
        user = super().save(commit=False)
        # Establece la contraseña de manera segura
        user.set_password(self.cleaned_data["password1"])
        # Si commit es True, guarda el usuario en la base de datos
        if commit:
            user.save()
        return user
    
    