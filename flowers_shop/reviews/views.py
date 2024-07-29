
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from flowers_shop.main.models import BaseOtziv, Tovar
from .forms import ReviewForm

@login_required
def add_review(request, tovar_id):
    tovar = get_object_or_404(Tovar, id=tovar_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ID_User = request.user
            review.ID_Tovar = tovar
            review.save()
            return redirect('tovar_detail', tovar_id=tovar.id)
    else:
        form = ReviewForm(initial={'ID_Tovar': tovar})
    return render(request, 'reviews/add_review.html', {'form': form, 'tovar': tovar})

def tovar_reviews(request, tovar_id):
    tovar = get_object_or_404(Tovar, id=tovar_id)
    reviews = BaseOtziv.objects.filter(ID_Tovar=tovar)
    return render(request, 'reviews/tovar_reviews.html', {'reviews': reviews, 'tovar': tovar})
