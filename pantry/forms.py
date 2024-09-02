from django import forms

from .models import Contact, Menu


class MenuForm(forms.ModelForm):
    category = forms.Select(attrs={"class": "d-none"})
    dish_name = forms.CharField(max_length=200, required=False, help_text="")
    dish_discription = forms.Textarea(
        attrs={
            "class": "form-control form-control-input mem-b-placeholder",
            "placeholder": "Description",
            "autocomplete": "off",
        }
    )
    dish_photo = forms.ImageField()

    class Meta:
        model = Menu
        fields = ("cafe", "category", "dish_name", "dish_discription", "dish_photo")


class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=300, required=False, help_text="")
    number_of_People = forms.IntegerField(required=False)
    date_of_booking = forms.DateField(required=False)
    message = forms.Textarea()
    phone_no = forms.IntegerField()

    class Meta:
        model = Contact
        fields = ("name", "number_of_People", "date_of_booking", "message", "phone_no")
