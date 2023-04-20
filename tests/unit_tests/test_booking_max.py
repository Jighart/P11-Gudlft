import server
from server import app


class TestBookMoreThanTwelvePlaces:

    client = app.test_client()
    competition = [
        {
            "name": "Test",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "40"
        }
    ]

    club = [
        {
            "name": "Test club",
            "email": "test@club.com",
            "points": "20"
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

    def test_more_than_twelve_total(self):
        booked = 8

        result = self.client.post(
            "/purchasePlaces",
            data={
                "places": booked,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        assert result.status_code == 403