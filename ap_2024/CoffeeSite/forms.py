from django import forms
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator

class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        max_length = 100,
        required = True,
        widget = forms.TextInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'jamshid@gmail.com  یا  jamshid_jamali'
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
    full_name = forms.CharField(
        max_length = 100,
        required = True,
        widget = forms.TextInput(attrs = {
            'placeholder' : 'جمشید جمالی'
        })
    )
    

    username = forms.CharField(
        max_length = 100,
        required = True,
        widget = forms.TextInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'jamshidjamali'
        })
    )

    email = forms.EmailField(
        required = True,
        widget = forms.EmailInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'jamshid@gmail.com'
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

class WarehouseManagementForm(forms.Form):
    sugar = forms.IntegerField(
        required = False,
        validators = [MinValueValidator(0)],
        widget = forms.NumberInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'sugar (g)'
        })
    )
    raw_coffee = forms.IntegerField(
        required = False,
        validators = [MinValueValidator(0)],
        widget = forms.NumberInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'raw coffee (g)'
        })
    )
    flour = forms.IntegerField(
        required = False,
        validators = [MinValueValidator(0)],
        widget = forms.NumberInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'flour (g)'
        })
    )
    chocolate = forms.IntegerField(
        required = False,
        validators = [MinValueValidator(0)],
        widget = forms.NumberInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'chocolate (g)'
        })
    )

class AddProductForm(forms.Form):
    name = forms.CharField(
        required = True,
        max_length = 100,
        widget = forms.TextInput(attrs = {
             'class': 'form-control',
            'placeholder': 'product name'
        })
    )
    sugar = forms.IntegerField(
        required = True,
        validators = [MinValueValidator(0)],
        widget = forms.NumberInput(attrs = {
             'class': 'form-control',
            'placeholder': 'sugar (g)'
        })
    )
    raw_coffee = forms.IntegerField(
        required = True,
        validators = [MinValueValidator(0)],
        widget = forms.NumberInput(attrs = {
             'class': 'form-control',
            'placeholder': 'raw coffee (g)'
        })
    )
    flour = forms.IntegerField(
        required = True,
        validators = [MinValueValidator(0)],
        widget = forms.NumberInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'flour (g)'
        })
    )
    chocolate = forms.IntegerField(
        required = True,
        validators = [MinValueValidator(0)],
        widget = forms.NumberInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'chocolate (g)'
        })
    )
    price = forms.FloatField(
        required = True,
        validators = [MinValueValidator(0)],
        widget = forms.NumberInput(attrs = {
           'class': 'form-control',
            'placeholder': 'price' 
        })
    )
    image = forms.ImageField(
        required = True,
        widget = forms.FileInput(attrs = {
            'class': 'form-control',
            'placeholder': 'image'
        })
    )
    product_verticals = [
        ('warm_drink', 'warm drink'),
        ('cold_drink', 'cold drink'),
        ('cake', 'cake')
    ]
    vertical = forms.ChoiceField(
        choices = product_verticals,
        required = True,
        widget = forms.Select(attrs = {
            'class' : 'form-control'
        })
    )