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
        booked = 13

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