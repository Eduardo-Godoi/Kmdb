import json

from rest_framework.test import APITestCase


class TestMovieView(APITestCase):
    def setUp(self):

        self.user_data = {
            "username": "user",
            "first_name": "Edward",
            "last_name": "Stewart",
            "password": "1234",
            "is_staff": False,
            "is_superuser": False,
        }

        self.user_login_data = {"username": "user", "password": "1234"}

        self.critic_data = {
            "username": "critic",
            "first_name": "Erick",
            "last_name": "Jacquin",
            "password": "1234",
            "is_staff": True,
            "is_superuser": False,
        }

        self.critic_login_data = {"username": "critic", "password": "1234"}

        self.admin_data = {
            "username": "admin",
            "first_name": "Jeff",
            "last_name": "Bezos",
            "password": "1234",
            "is_staff": True,
            "is_superuser": True,
        }

        self.admin_login_data = {"username": "admin", "password": "1234"}

        self.movie_data = {
            "title": "O Poderoso Chefão",
            "duration": "175m",
            "genres": [{"name": "Crime"}, {"name": "Drama"}],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma 'família' de Nova York que está feliz, pois Connie (Talia Shire), sua filha,se casou com Carlo (Gianni Russo). Por ser seu padrinho Vito foi procurar o líder da banda e ofereceu 10 mil dólares para deixar Johnny sair, mas teve o pedido recusado.",
        }

        self.movie_data_2 = {
            "title": "Um Sonho de liberdade",
            "duration": "142m",
            "genres": [{"name": "Ficção Científica"}, {"name": "Drama"}],
            "premiere": "1994-10-14",
            "classification": 14,
            "synopsis": "Andy Dufresne é condenado a duas prisões perpétuas consecutivas pelas mortes de sua esposa e de seu amante. Porém, só Andy sabe que ele não cometeu os crimes. No presídio, durante dezenove anos, ele faz amizade com Red, sofre as brutalidades da vida na cadeia, se adapta, ajuda os carcereiros, etc.",
        }

        self.movie_data_3 = {
            "title": "Em busca de liberdade",
            "duration": "175m",
            "genres": [{"name": "Obra de época"}, {"name": "Drama"}],
            "premiere": "2018-02-22",
            "classification": 14,
            "synopsis": "Representando a Grã-Bretanha,  corredor Eric Liddell (Joseph Fiennes) ganha uma medalha de ouro nas Olimpíadas de Paris em 1924. Ele decide ir até a China para trabalhar como missionário e acaba encontrando um país em guerra. Com a invasão japonesa no território chinês durante a Segunda Guerra Mundial, Liddell acaba em um campo de concentração.",
        }

    def test_admin_can_create_movie(self):
        self.client.post("/api/accounts/", self.admin_data, format="json")

        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        movie = self.client.post("/api/movies/", self.movie_data, format="json")
        self.assertEqual(movie.json()["id"], 1)
        self.assertEqual(movie.status_code, 201)

    def test_critic_cannot_create_movie(self):
        self.client.post("/api/accounts/", self.critic_data, format="json")

        token = self.client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        status_code = self.client.post(
            "/api/movies/", self.movie_data, format="json"
        ).status_code
        self.assertEqual(status_code, 403)

    def test_user_cannot_create_movie(self):
        self.client.post("/api/accounts/", self.user_data, format="json")

        token = self.client.post(
            "/api/login/", self.user_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        status_code = self.client.post(
            "/api/movies/", self.movie_data, format="json"
        ).status_code

        self.assertEqual(status_code, 403)

    def test_anonymous_cannot_create_movie(self):
        response = self.client.post(
            "/api/movies/", self.movie_data, format="json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_anonymous_can_list_movies(self):
        self.client.post("/api/accounts/", self.admin_data, format="json")

        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        movies_list = self.client.get("/api/movies/", format="json").json()
        self.assertEqual(len(movies_list), 1)


    def test_filter_movies_with_the_filter_request(self):
        self.client.post("/api/accounts/", self.admin_data, format="json")

        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        movie_1 = self.client.post(
            "/api/movies/", self.movie_data, format="json"
        ).json()

        movie_2 = self.client.post(
            "/api/movies/", self.movie_data_2, format="json"
        ).json()

        movie_2 = self.client.post(
            "/api/movies/", self.movie_data_3, format="json"
        ).json()

        filter_movies = self.client.generic(
            method="GET",
            path="/api/movies/",
            data=json.dumps({"title": "liberdade"}),
            content_type="application/json",
        )

        self.assertEqual(len(filter_movies.json()), 3)
        self.assertEqual(filter_movies.status_code, 200)

    def test_output_format_data(self):
        self.client.post("/api/accounts/", self.admin_data, format="json")

        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        movie_1 = self.client.post(
            "/api/movies/", self.movie_data, format="json"
        ).json()

        output_format_movie_data = {
            "id": 1,
            "title": "O Poderoso Chefão",
            "duration": "175m",
            "genres": [{"id": 1, "name": "Crime"}, {"id": 2, "name": "Drama"}],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma 'família' de Nova York que está feliz, pois Connie (Talia Shire), sua filha,se casou com Carlo (Gianni Russo). Por ser seu padrinho Vito foi procurar o líder da banda e ofereceu 10 mil dólares para deixar Johnny sair, mas teve o pedido recusado.",
        }

        self.assertEqual(movie_1, output_format_movie_data)


class TestMovieViewByIdGetDelete(APITestCase):
    def setUp(self):

        self.user_data = {
            "username": "user",
            "first_name": "Edward",
            "last_name": "Stewart",
            "password": "1234",
            "is_staff": False,
            "is_superuser": False,
        }

        self.user_login_data = {"username": "user", "password": "1234"}

        self.critic_data = {
            "username": "critic",
            "first_name": "Erick",
            "last_name": "Jacquin",
            "password": "1234",
            "is_staff": True,
            "is_superuser": False,
        }

        self.critic_login_data = {"username": "critic", "password": "1234"}

        self.admin_data = {
            "username": "admin",
            "first_name": "Jeff",
            "last_name": "Bezos",
            "password": "1234",
            "is_staff": True,
            "is_superuser": True,
        }

        self.admin_login_data = {"username": "admin", "password": "1234"}

        self.movie_data = {
            "title": "O Poderoso Chefão",
            "duration": "175m",
            "genres": [{"name": "Crime"}, {"name": "Drama"}],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma 'família' de Nova York que está feliz, pois Connie (Talia Shire), sua filha,se casou com Carlo (Gianni Russo). Por ser seu padrinho Vito foi procurar o líder da banda e ofereceu 10 mil dólares para deixar Johnny sair, mas teve o pedido recusado.",
        }

        self.movie_data_2 = {
            "title": "Um Sonho de liberdade",
            "duration": "142m",
            "genres": [{"name": "Ficção Científica"}, {"name": "Drama"}],
            "premiere": "1994-10-14",
            "classification": 14,
            "synopsis": "Andy Dufresne é condenado a duas prisões perpétuas consecutivas pelas mortes de sua esposa e de seu amante. Porém, só Andy sabe que ele não cometeu os crimes. No presídio, durante dezenove anos, ele faz amizade com Red, sofre as brutalidades da vida na cadeia, se adapta, ajuda os carcereiros, etc.",
        }

        self.movie_data_3 = {
            "title": "Em busca de liberdade",
            "duration": "175m",
            "genres": [{"name": "Obra de época"}, {"name": "Drama"}],
            "premiere": "2018-02-22",
            "classification": 14,
            "synopsis": "Representando a Grã-Bretanha,  corredor Eric Liddell (Joseph Fiennes) ganha uma medalha de ouro nas Olimpíadas de Paris em 1924. Ele decide ir até a China para trabalhar como missionário e acaba encontrando um país em guerra. Com a invasão japonesa no território chinês durante a Segunda Guerra Mundial, Liddell acaba em um campo de concentração.",
        }

    def test_anonymous_can_filter_movies(self):
        self.client.post("/api/accounts/", self.admin_data, format="json")

        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        self.client.post("/api/movies/", self.movie_data, format="json")


        movies_filter = self.client.get("/api/movies/1/", format="json")

        self.assertEqual(movies_filter.status_code, 200)
        self.assertEqual(movies_filter.json()["id"], 1)

    def test_anonymous_cannot_filter_movies_with_the_invalid_movie_id(self):
        movies_filter = self.client.get("/api/movies/99/", format="json")
        self.assertEqual(movies_filter.status_code, 404)
        self.assertEqual(movies_filter.json(), {"detail": "Not found."})

    def test_critic_cannot_delete_movies(self):
        self.client.post("/api/accounts/", self.critic_data, format="json")

        token = self.client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        status_code = self.client.delete("/api/movies/1/", format="json").status_code
        self.assertEqual(status_code, 403)
        
    def test_user_cannot_delete_movies(self):
        self.client.post("/api/accounts/", self.user_data, format="json")

        token = self.client.post(
            "/api/login/", self.user_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        status_code = self.client.delete("/api/movies/1/", format="json").status_code
        self.assertEqual(status_code, 403)


    def test_admin_can_delete_movie(self):
        self.client.post("/api/accounts/", self.admin_data, format="json")

        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        movies = self.client.get("/api/movies/", format="json")
        self.assertEqual(len(movies.json()), 1)

        status_code = self.client.delete("/api/movies/1/", format="json").status_code
        self.assertEqual(status_code, 204)

        movies = self.client.get("/api/movies/", format="json")
        self.assertEqual(len(movies.json()), 0)
        self.assertEqual(movies.json(), [])


class TestReviewView(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "user",
            "password": "1234",
            "first_name": "John",
            "last_name": "Doe",
            "is_superuser": False,
            "is_staff": False,
        }

        self.user_login_data = {
            "username": "user",
            "password": "1234",
        }

        self.critic_data = {
            "username": "critic",
            "password": "1234",
            "first_name": "John",
            "last_name": "Doe",
            "is_superuser": False,
            "is_staff": True,
        }

        self.critic_login_data = {
            "username": "critic",
            "password": "1234",
        }

        self.admin_data = {
            "username": "admin",
            "password": "1234",
            "first_name": "John",
            "last_name": "Doe",
            "is_superuser": True,
            "is_staff": True,
        }

        self.admin_login_data = {
            "username": "admin",
            "password": "1234",
        }

        self.movie_data_1 = {
            "title": "O Poderoso Chefão",
            "duration": "175m",
            "genres": [{"name": "Crime"}, {"name": "Drama"}],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma 'família' de Nova York que está feliz, pois Connie (Talia Shire), sua filha,se casou com Carlo (Gianni Russo). Por ser seu padrinho Vito foi procurar o líder da banda e ofereceu 10 mil dólares para deixar Johnny sair, mas teve o pedido recusado.",
        }

        self.movie_data_2 = {
            "title": "Um Sonho de Liberdade",
            "duration": "142m",
            "genres": [{"name": "Drama"}, {"name": "Ficção científica"}],
            "premiere": "1994-10-14",
            "classification": 16,
            "synopsis": "Andy Dufresne é condenado a duas prisões perpétuas consecutivas pelas mortes de sua esposa e de seu amante. Porém, só Andy sabe que ele não cometeu os crimes. No presídio, durante dezenove anos, ele faz amizade com Red, sofre as brutalidades da vida na cadeia, se adapta, ajuda os carcereiros, etc.",
        }
        self.review_data_1 = {
            "stars": 2,
            "review": "Muito fraco",
            "spoilers": False,
        }

        self.review_data_2 = {
            "stars": 10,
            "review": "Ótimo filme. Adorei a parte em que o fulaninho resgatou a fulaninha",
            "spoilers": True,
        }

        self.wrong_review_data = {
            "stars": 20,
            "review": "Muito fraco",
            "spoilers": False,
        }

    def test_critic_can_create_review(self):

        self.client.post("/api/accounts/", self.admin_data, format="json").json()
        self.client.post("/api/accounts/", self.critic_data, format="json").json()

        token = self.client.post("/api/login/", self.admin_login_data, format="json").json()[
            "token"
        ]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        self.client.post("/api/movies/", self.movie_data_1, format="json")

        token = self.client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post(
            "/api/movies/1/review/", self.review_data_1, format="json"
        )

        expected_review_response = {
            "id": 1,
            "critic": {"id": 2, "first_name": "John", "last_name": "Doe"},
            "stars": 2,
            "review": "Muito fraco",
            "spoilers": False,
        }

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), expected_review_response)

    def test_user_cannot_create_review(self):

        self.client.post("/api/accounts/", self.admin_data, format="json").json()
        self.client.post("/api/accounts/", self.user_data, format="json").json()

        token = self.client.post("/api/login/", self.admin_login_data, format="json").json()[
            "token"
        ]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        self.client.post("/api/movies/", self.movie_data_1, format="json")

        token = self.client.post("/api/login/", self.user_login_data, format="json").json()[
            "token"
        ]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post(
            "/api/movies/1/review/", self.review_data_1, format="json"
        )
        self.assertEqual(response.status_code, 403)

    def test_admin_cannot_create_review(self):
        self.client.post("/api/accounts/", self.admin_data, format="json").json()
        token = self.client.post("/api/login/", self.admin_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        self.client.post("/api/movies/", self.movie_data_1, format="json")
        response = self.client.post(
            "/api/movies/1/review/", self.review_data_1, format="json"
        )
        self.assertEqual(response.status_code, 403)

    def test_create_review_without_movie(self):

        self.client.post("/api/accounts/", self.critic_data, format="json")

        token = self.client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post(
            "/api/movies/1/review/", self.review_data_1, format="json"
        )
        self.assertEqual(response.status_code, 404)

    def test_update_review_that_doesnt_exist(self):

        self.client.post("/api/accounts/", self.admin_data, format="json").json()
        self.client.post("/api/accounts/", self.critic_data, format="json").json()

        token = self.client.post("/api/login/", self.admin_login_data, format="json").json()[
            "token"
        ]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        self.client.post("/api/movies/", self.movie_data_1, format="json")

        token = self.client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.put(
            "/api/movies/1/review/", self.review_data_2, format="json"
        )
        self.assertEqual(response.status_code, 404)        

    def test_critic_can_update_review_sucess(self):

        self.client.post("/api/accounts/", self.admin_data, format="json").json()
        self.client.post("/api/accounts/", self.critic_data, format="json").json()

        token = self.client.post("/api/login/", self.admin_login_data, format="json").json()[
            "token"
        ]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        self.client.post("/api/movies/", self.movie_data_1, format="json")
        self.client.post("/api/movies/", self.movie_data_2, format="json")

        token = self.client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post(
            "/api/movies/1/review/", self.review_data_1, format="json"
        )

        response = self.client.put(
            "/api/movies/1/review/", self.review_data_2, format="json"
        )
        expected_review_response = {
            "id": 1,
            "critic": {"id": 2, "first_name": "John", "last_name": "Doe"},
            "stars": 10,
            "review": "Ótimo filme. Adorei a parte em que o fulaninho resgatou a fulaninha",
            "spoilers": True,
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_review_response)

        response = self.client.get("/api/movies/1/").json()
        expected_reviews = [
            {
                "id": 1,
                "critic": {"id": 2, "first_name": "John", "last_name": "Doe"},
                "stars": 10,
                "review": "Ótimo filme. Adorei a parte em que o fulaninho resgatou a fulaninha",
                "spoilers": True,
            }
        ]
        self.assertEqual(len(response["reviews"]), 1)
        self.assertEqual(response["reviews"], expected_reviews)

    def test_update_review_unexisting_movie(self):

        self.client.post("/api/accounts/", self.admin_data, format="json").json()
        self.client.post("/api/accounts/", self.critic_data, format="json").json()
        self.client.post("/api/accounts/", self.user_data, format="json").json()

        token = self.client.post("/api/login/", self.admin_login_data, format="json").json()[
            "token"
        ]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        token = self.client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.put(
            "/api/movies/1/review/", self.review_data_2, format="json"
        )
        self.assertEqual(response.status_code, 404)


class TestListReview(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "user",
            "password": "1234",
            "first_name": "John",
            "last_name": "Doe",
            "is_superuser": False,
            "is_staff": False,
        }

        self.user_login_data = {
            "username": "user",
            "password": "1234",
        }

        self.critic_data = {
            "username": "critic",
            "password": "1234",
            "first_name": "Bruce",
            "last_name": "Wayne",
            "is_superuser": False,
            "is_staff": True,
        }
        

        self.critic_login_data = {
            "username": "critic",
            "password": "1234",
        }

        self.critic_data_2 = {
            "username": "critic2",
            "password": "1234",
            "first_name": "Clark",
            "last_name": "Kent",
            "is_superuser": False,
            "is_staff": True,
        }
        

        self.critic_login_data_2 = {
            "username": "critic2",
            "password": "1234",
        }

        self.admin_data = {
            "username": "admin",
            "password": "1234",
            "first_name": "John",
            "last_name": "Doe",
            "is_superuser": True,
            "is_staff": True,
        }

        self.admin_login_data = {
            "username": "admin",
            "password": "1234",
        }

        self.movie_data_1 = {
            "title": "O Poderoso Chefão",
            "duration": "175m",
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma 'família' de Nova York que está feliz, pois Connie (Talia Shire), sua filha,se casou com Carlo (Gianni Russo). Por ser seu padrinho Vito foi procurar o líder da banda e ofereceu 10 mil dólares para deixar Johnny sair, mas teve o pedido recusado.",
        }

        self.review_data_1 = {
            "stars": 2,
            "review": "Podia ser muito melhor",
            "spoilers": False,
        }

        self.review_data_2 = {
            "stars": 10,
            "review": "Melhor filme que ja assisti",
            "spoilers": True,
        }

        self.movie_data_1 = {
            "title": "O Poderoso Chefão",
            "duration": "175m",
            "genres": [{"name": "Crime"}, {"name": "Drama"}],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma 'família' de Nova York que está feliz, pois Connie (Talia Shire), sua filha,se casou com Carlo (Gianni Russo). Por ser seu padrinho Vito foi procurar o líder da banda e ofereceu 10 mil dólares para deixar Johnny sair, mas teve o pedido recusado.",
        }

    def test_anonymous_cannot_view_reviews(self):

        response = self.client.get("/api/reviews/")
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_user_cannot_view_reviews(self):

        self.client.post("/api/accounts/", self.user_data, format="json").json()

        token = self.client.post("/api/login/", self.user_login_data, format="json").json()[
            "token"
        ]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.get("/api/reviews/")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {'detail': 'You do not have permission to perform this action.'},
        )

    def test_critic_can_view_only_own_reviews(self):

        self.client.post("/api/accounts/", self.admin_data, format="json").json()

        self.client.post("/api/accounts/", self.critic_data, format="json").json()
        self.client.post("/api/accounts/", self.critic_data_2, format="json").json()

        token = self.client.post("/api/login/", self.admin_data, format="json").json()[
            "token"
        ]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        self.client.post("/api/movies/", self.movie_data_1, format="json")

        token = self.client.post("/api/login/", self.critic_login_data, format="json").json()[
            "token"
        ]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post(
            "/api/movies/1/review/", self.review_data_1, format="json"
        )

        token = self.client.post("/api/login/", self.critic_login_data_2, format="json").json()[
            "token"
        ]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post(
            "/api/movies/1/review/", self.review_data_2, format="json"
        )

        token = self.client.post("/api/login/", self.critic_login_data, format="json").json()[
            "token"
        ]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.get("/api/reviews/")

        review_1 = {
            'id': 1,
            'stars': 2,
            'review': 'Podia ser muito melhor',
            'spoilers': False
        }

        critic_1 = {
            'first_name': 'Bruce',
            'last_name': 'Wayne'
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertDictContainsSubset(review_1, response.json()[0])
        self.assertDictContainsSubset(critic_1, response.json()[0]['critic'])

        review_2 = {
            'id': 2,
            'stars': 10,
            'review': 'Melhor filme que ja assisti',
            'spoilers': True
        }

        critic_2 = {
            'first_name': 'Clark',
            'last_name': 'Kent'
        }

        token = self.client.post("/api/login/", self.critic_login_data_2, format="json").json()[
            "token"
        ]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        response = self.client.get("/api/reviews/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertDictContainsSubset(review_2, response.json()[0])
        self.assertDictContainsSubset(critic_2, response.json()[0]['critic'])

    def test_admin_can_view_all_reviews(self):

        self.client.post("/api/accounts/", self.admin_data, format="json").json()

        self.client.post("/api/accounts/", self.critic_data, format="json").json()
        self.client.post("/api/accounts/", self.critic_data_2, format="json").json()

        token = self.client.post("/api/login/", self.admin_data, format="json").json()[
            "token"
        ]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        self.client.post("/api/movies/", self.movie_data_1, format="json")

        token = self.client.post("/api/login/", self.critic_login_data, format="json").json()[
            "token"
        ]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post(
            "/api/movies/1/review/", self.review_data_1, format="json"
        )

        token = self.client.post("/api/login/", self.critic_login_data_2, format="json").json()[
            "token"
        ]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post(
            "/api/movies/1/review/", self.review_data_2, format="json"
        )

        token = self.client.post("/api/login/", self.admin_login_data, format="json").json()[
            "token"
        ]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.get("/api/reviews/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

        critic_1 = {
            'first_name': 'Bruce',
            'last_name': 'Wayne'
        }

        self.assertDictContainsSubset(critic_1, response.json()[0]['critic'])

        critic_2 = {
            'first_name': 'Clark',
            'last_name': 'Kent'
        }

        self.assertDictContainsSubset(critic_2, response.json()[1]['critic'])
