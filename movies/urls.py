# from django.urls import path

# from movies.views import (MovieDetailView, MovieViews, ReviewDetailView,
#                           ReviewView)

# urlpatterns = [
#     path('movies/', MovieViews.as_view()),
#     path('movies/<int:movie_id>/', MovieDetailView.as_view()),
#     path('movies/<int:movie_id>/review/', ReviewDetailView.as_view()),
#     path('reviews/', ReviewView.as_view()),

from rest_framework.routers import SimpleRouter

# ]
from .views import ListReview, MovieViews

router = SimpleRouter()
router.register(prefix=r'movies', viewset=MovieViews)
router.register(prefix=r'reviews', viewset=ListReview)


urlpatterns = router.urls

print(urlpatterns)
