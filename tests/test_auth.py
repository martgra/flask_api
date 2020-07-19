from flaskapi.auth import api_key


def test_auth():
    assert api_key.auth("asdf1234567890", None)["uid"] == 100