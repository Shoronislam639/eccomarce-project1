from django import forms
from core.models import ProductReviews


class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Write Review"})
    )

    class Meta:
        model = ProductReviews
        fields = ('review', 'rating')
