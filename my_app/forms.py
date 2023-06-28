from .models import Listing

from django import forms

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = [ "owner", "saved", "lot", "long"]
        labels = {
            'description': '', 
            'lot': '',
            'long': '',
            'price': '',
            'bed': '',
            'bath': '',
            'year_built': '', 
            'image': '',
            'address': ''
        }
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Descripton'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Price'}),
            'bed': forms.NumberInput(attrs={'placeholder': 'Bed'}),
            'bath': forms.NumberInput(attrs={'placeholder': 'Bath'}),
            'year_built': forms.NumberInput(attrs={'placeholder': 'Year Built'}), 
            'address': forms.TextInput(attrs={'placeholder': 'Address'})
        }
        
  
class FindForm(forms.Form):
    find_input = forms.CharField(label="", max_length=100, 
        widget=forms.TextInput(attrs={"placeholder": "Enter an address, city or ZIP code"}))