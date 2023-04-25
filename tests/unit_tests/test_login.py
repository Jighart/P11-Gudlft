import server
from server import app


class TestLogin:
    client = app.test_client()

    def test_valid_email(self):
        result = self.client.post("/showSummary", data={"email": server.clubs[0]["email"]})
        assert result.status_code == 200
        assert f"{server.clubs[0]['email']}" in result.data.decode()

    def test_invalid_email(self):
        result = self.client.post("/showSummary", data={"email": "jhbdfkshdvf"})
        assert result.status_code == 401
        assert "No account found with this email" in result.data.decode()

    def test_empty_email(self):
        result = self.client.post("/showSummary", data={"email": ""})
        assert result.status_code == 401
        assert "Please enter your email" in result.data.decode()

    def test_login(self):
        result = self.client.get("/")
        assert result.status_code == 200

    def test_logout(self):
        result = self.client.get("/logout")
        assert result.status_code == 302