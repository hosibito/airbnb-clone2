from django import forms

from django_countries.fields import CountryField

from . import models


class SearchForm(forms.Form):

    # city = forms.CharField(initial="Anywhere", widget=forms.Textarea)
    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="KR").formfield()  # django_countries 깃허브 문서에 있슴.
    room_type = forms.ModelChoiceField(
        required=False,
        empty_label="Any kinds",
        queryset=models.RoomType.objects.all(),
    )
    price = forms.IntegerField(
        required=False,
        min_value=1,
    )
    guests = forms.IntegerField(required=False, min_value=1, max_value=10)
    bedrooms = forms.IntegerField(
        required=False,
        min_value=1,
    )
    beds = forms.IntegerField(
        required=False,
        min_value=1,
    )
    baths = forms.IntegerField(
        required=False,
        min_value=1,
    )
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    houserules = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.HouseRule.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ("caption", "file")

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        # print(pk)
        room = models.Room.objects.get(pk=pk)
        photo.room = room
        photo.save()
