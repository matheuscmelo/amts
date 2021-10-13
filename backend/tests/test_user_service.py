from services import user_service

def test_request_password_reset():
    r = user_service.create_user(email='test@test.com', password="aaaaa", user_type=1, phone=None, address=None,
                                 professional_email=None, professional_title=None)
    user = r.approve()
    request = user_service.request_password_reset(id=user.id)
    assert request.user_id == user.id
    assert request.user == user


def test_reset_password():
    r = user_service.create_user(email='test@test.com', password="aaaaa", user_type=1, phone=None, address=None,
                                 professional_email=None, professional_title=None)
    user = r.approve()
    request = user_service.request_password_reset(id=user.id)
    user_service.reset_password(token=request.token, password='bbbbb')
    user = user_service.get_user(user.id)
    assert user.password == 'bbbbb'


def test_get_user():
    r = user_service.create_user(email='test@test.com', password="aaaaa", user_type=1, phone=None, address=None,
                             professional_email=None, professional_title=None)
    user = r.approve()
    assert user is not None
    assert user.email == 'test@test.com'
    assert user.user_type == 1
