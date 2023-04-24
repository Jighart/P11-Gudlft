import server
from server import app


class TestBookPastCompetition:

    client = app.test_client()
    competitions = [
        {
            "name": "Test_closed",
            "date": "2021-04-27 10:00:00",
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
        assert result.status_code == 403

    def test_book_open_competition(self):
        result = self.client.get(
            f"/book/{self.competitions[1]['name']}/{self.club[0]['name']}"
        )
        assert result.status_code == 200