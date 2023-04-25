import server
from server import app


class TestBookMoreThanTwelvePlaces:

    client = app.test_client()
    competition = [
        {
            "name": "Test comp",
            "date": "2024-04-20 10:00:00",
            "numberOfPlaces": "24"
        }
    ]

    club = [
        {
            "name": "Test club",
            "email": "test@club.com",
            "points": "30"
        }
    ]

    places_booked = [
        {
            "competition": "Test comp",
            "booked": [5, "Test club"]
        }
    ]

    def setup_method(self):
        server.competitions = self.competition
        server.clubs = self.club
        server.places_booked = self.places_booked

    def test_less_than_twelve(self):
        booked = 5

        result = self.client.post(
            "/purchasePlaces",
            data={
                "places": booked,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        assert result.status_code == 200

    def test_more_than_twelve(self):
        booked = 15

        result = self.client.post(
            "/purchasePlaces",
            data={
                "places": booked,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        assert result.status_code == 403
        assert "You can&#39;t book more than 12 places in a competition." in result.data.decode()

    def test_more_than_twelve_added(self):
        booked = 10

        result = self.client.post(
            "/purchasePlaces",
            data={
                "places": booked,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        assert result.status_code == 403
        assert "You can&#39;t book more than 12 places in a competition." in result.data.decode()

    def test_more_than_open_places(self):
        booked = 25

        result = self.client.post(
            "/purchasePlaces",
            data={
                "places": booked,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        assert result.status_code == 403
        assert "Not enough open places in the competition" in result.data.decode()


class TestBookPastCompetition:

    client = app.test_client()
    competitions = [
        {
            "name": "Test_closed",
            "date": "2020-04-27 10:00:00",
            "numberOfPlaces": "20"
        },
        {
            "name": "Test_open",
            "date": "2024-04-27 10:00:00",
            "numberOfPlaces": "20"
        }
    ]

    club = [
        {
            "name": "Test club",
            "email": "test@club.com",
            "points": "15"
        }
    ]

    def setup_method(self):
        server.competitions = self.competitions
        server.clubs = self.club

    def test_book_closed_competition(self):
        result = self.client.get(
            f"/book/{self.competitions[0]['name']}/{self.club[0]['name']}"
        )
        assert result.status_code == 400

    def test_book_open_competition(self):
        result = self.client.get(
            f"/book/{self.competitions[1]['name']}/{self.club[0]['name']}"
        )
        assert result.status_code == 200

    def test_book_inexistant_competition(self):
        result = self.client.get(
            f"/book/X/{self.club[0]['name']}"
        )
        assert result.status_code == 404

