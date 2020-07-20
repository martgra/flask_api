"""Mocking API_KEY method for connexion authentication"""
from connexion.exceptions import OAuthProblem

TOKEN_DB = {"asdf1234567890": {"uid": 100}}


def auth(token, required_scopes):
    """Authenticate API_KEY token"""
    info = TOKEN_DB.get(token, None)

    if not info:
        raise OAuthProblem("Invalid token")
    return info
