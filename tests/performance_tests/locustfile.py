import json
from locust import HttpUser, task, between


def load_clubs():
    with open('../../clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('../../competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


class LocustTestServer(HttpUser):
    wait_time = between(1, 3)
    competition = load_competitions()[0]
    club = load_clubs()[0]

    def on_start(self):
        self.client.get("/", name=".index")
        self.client.post("/showSummary", data={'email': self.club["email"]}, name=".show_summary")

    @task
    def get_booking(self):
        self.client.get(
            f"/book/{self.competition['name']}/{self.club['name']}",
            name="book"
        )

    @task
    def post_booking(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "places": 0,
                "club": self.club["name"],
                "competition": self.competition["name"]
            },
            name="purchase_places"
        )

    @task
    def get_board(self):
        self.client.get("/showPointBoard", name="view_clubs")
