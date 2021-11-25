# from accounts.models import User
# from django.test import TestCase
# from movies.models import Genre, Movie, Review


# class MovieModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.title = "O Poderoso Chefão"
#         cls.duration = "175m"
#         cls.premiere = "1972-09-10"
#         cls.classification = 14
#         cls.synopsis = "Don Vito Corleone é o chefe de uma 'família'..."

#         cls.movie = Movie.objects.create(
#             title=cls.title,
#             duration=cls.duration,
#             premiere=cls.premiere,
#             classification=cls.classification,
#             synopsis=cls.synopsis
#         )
#         cls.list_genre = [{"name": "Crime"}, {"name": "Drama"}, {"name": "Mafia"}]

#         for g in cls.list_genre:
#             cls.genre = Genre.objects.create(name=g['name'])
#             cls.movie.genres.add(cls.genre)

#         cls.genres = Genre.objects.all()

#     def test_movie_fields(self):
#         self.assertIsInstance(self.movie.title, str)
#         self.assertEqual(self.movie.title, self.title)

#         self.assertIsInstance(self.movie.duration, str)
#         self.assertEqual(self.movie.duration, self.duration)

#         self.assertIsInstance(self.movie.premiere, str)
#         self.assertEqual(self.movie.premiere, self.premiere)

#         self.assertIsInstance(self.movie.classification, int)
#         self.assertEqual(self.movie.classification, self.classification)

#         self.assertIsInstance(self.movie.synopsis, str)
#         self.assertEqual(self.movie.synopsis, self.synopsis)

#     def test_genre_field(self):
#         self.assertIsInstance(self.genre.name, str)
#         self.assertEqual(len(self.genres), self.movie.genres.count())

#     def test_movie_genre_relationship(self):
#         self.assertEqual(len(self.list_genre), self.movie.genres.count())

#     def test_review_movie_relationship(self):
#         user = User.objects.create_user(
#             username='user',
#             password='1234',
#             first_name='Jhon',
#             last_name='Wick',
#             is_superuser=False,
#             is_staff=True 
#         )

#         reviews = [
#             Review.objects.create(
#                 stars=7,
#                 review=f'review {i}',
#                 spoilers=False,
#                 critic=user,
#                 movie=self.movie
#             )for i in range(4)
#         ]

#         self.assertEqual(len(reviews), self.movie.reviews.count())
