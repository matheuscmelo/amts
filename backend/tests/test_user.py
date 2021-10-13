from models import User, UserCreationRequest

def test_user_create():
    u = User(email='test@test.com', password='0101001', user_type=1)
    assert u.email == 'test@test.com'


def test_user_forget():
    u1 = User(email='test@test.com', password='0101001', user_type=1)
    u1.be_forgotten()
    assert u1.forgotten


def test_user_request():
    request = UserCreationRequest(email='test@test.com', password='0101001', user_type=1)
    user = request.approve()
    assert user is not None
    assert isinstance(user, User)
    assert user.email == 'test@test.com'
    assert user.password == '0101001'
