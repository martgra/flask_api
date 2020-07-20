import json
from flaskapi.models import User


def test_get_user(client, db, user):
    # test 404
    rep = client.get("user/100000")
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    # test get_user
    rep = client.get("user/{}".format(user.id))
    assert rep.status_code == 200

    data = rep.get_json()["user"]
    assert data["username"] == user.username
    assert data["email"] == user.email
    assert data["active"] == user.active


def test_put_user(client, db, user):
    data = {"username": "updated"}

    # test 404
    rep = client.put("user/100000", json=data)
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    # test update user
    rep = client.put("user/{}".format(user.id), json=data)
    assert rep.status_code == 200

    data = rep.get_json()["user"]
    assert data["username"] == "updated"
    assert data["email"] == user.email
    assert data["active"] == user.active


def test_delete_user(client, db, user):
    # test 404
    rep = client.delete("user/100000")
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    # test get_user

    rep = client.delete("user/{}".format(user.id))
    assert rep.status_code == 200
    assert db.session.query(User).filter_by(id=user.id).first() is None

    data = rep.get_json()
    assert data["message"] == "user deleted"


def test_create_user(client, db):
    # test bad data
    data = {"username": "created"}
    rep = client.post("user", json=data)
    assert rep.status_code == 400

    data["password"] = "admin1234"
    data["email"] = "create@mail.com"

    rep = client.post("user", json=data)
    assert rep.status_code == 201

    data = rep.get_json()
    user = db.session.query(User).filter_by(id=data["user"]["id"]).first()

    assert user.username == "created"
    assert user.email == "create@mail.com"


def test_get_all_user(client, db, user_factory):
    users = user_factory.create_batch(30)
    db.session.add_all(users)
    db.session.commit()

    rep = client.get("user")
    assert rep.status_code == 200

    results = rep.get_json()
    for user in users:
        assert any(u["id"] == user.id for u in results["users"])


def test_secret(client, db):
    # Test invalid token
    rep = client.get("secret", headers={"X-Auth": "sdf1234567890"})
    assert rep.status_code == 401

    rep = client.get("secret", headers={"X-Auth": "asdf1234567890"})
    assert rep.status_code == 200
