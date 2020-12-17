from .models import Listing, Bid, Comment
from django import forms


class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "categories",
            "price",
            "image",
        ]


class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = ["price"]


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["comment"]
