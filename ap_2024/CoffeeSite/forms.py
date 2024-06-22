from django import forms
from django.core.validators import RegexValidator

class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        max_length = 100,
        required = True,
        widget = forms.TextInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'username or email'
        })
    )
    
    password = forms.CharField(
        max_length = 100,
        widget = forms.PasswordInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'password'
        })

    )

class SignupForm(forms.Form):
    first_name = forms.CharField(
        max_length = 100,
        required = True,
        widget = forms.TextInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'first name'
        })
    )
    
    last_name = forms.CharField(
        max_length = 100,
        required = True,
        widget = forms.TextInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'last name'
        })
    )

    username = forms.CharField(
        max_length = 100,
        required = True,
        widget = forms.TextInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'username'
        })

    )

    email = forms.EmailField(
        required = True,
        widget = forms.EmailInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'email'
        })
    )

    password = forms.CharField(
        max_length = 100,
        required = True,
        widget = forms.PasswordInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'password'
        }),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
                message='password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number, and one special character.'
            )
        ]
    )

    password_confirm = forms.CharField(
       max_length = 50,
       required = True,
       widget = forms.PasswordInput(attrs = {
        'class' : 'form-control',
        'placeholder' : 'password'
       })
    )
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            self.add_error('password_confirm', 'passwords do not mach.')
        return cleaned_data
