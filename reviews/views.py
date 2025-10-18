from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm

@login_required
def submit_review(request, product_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user_id = request.user.id
            review.product_id = product_id
            review.save()
            return redirect('product_detail', product_id=product_id)
    else:
        form = ReviewForm()
    return render(request, 'reviews/submit_review.html', {'form': form})

def view_reviews(request, product_id):
    reviews = Review.objects.filter(product_id=product_id)
    return render(request, 'reviews/view_reviews.html', {'reviews': reviews})