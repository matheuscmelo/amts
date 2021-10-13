from services import email_service
from models import User, UserCreationRequest, PasswordResetRequest, UserImage, Interaction
from exceptions import Unauthorized, BadRequest, NotFound
from utils import generate_random_string


user_api_fields = User.api_fields
user_request_api_fields = UserCreationRequest.api_fields
interaction_api_fields = Interaction.api_fields

def create_user(email, password, user_type, phone, address, professional_email, professional_title, image=None, *args, **kwargs):

    images = []

    if image is not None:
        image = UserImage(image=image.encode())
        image.save()
        images = [image.id]

    user = UserCreationRequest(email=email, password=password, user_type=user_type, phone=phone,
                               address=address, professional_email=professional_email,
                               professional_title=professional_title, images=images)
    user.save()

    return user

def request_password_reset(email):
    user = get_user_by_email(email)
    r = PasswordResetRequest(user_id=user.id, user=user, token=generate_random_string(32))
    r.save()
    email_service.send_password_reset_email(user, r.token)
    return r


def reset_password(token, password):
    r = get_password_reset_request(token)
    user = r.user
    user.password = password
    user.save()
    return user


def get_password_reset_request(token):
    request = PasswordResetRequest.query.get(token)
    if request is None:
        raise NotFound(f'Password reset request with token {token} was not found')
    return request


def approve_request(id, request_id):
    user = get_user(id)
    if user.user_type == User.OPERATOR:
        request = get_user_request(request_id)
        if request.evaluated:
            raise BadRequest("Request already evaluated")
        user = request.approve()
        return user
    else:
        raise Unauthorized("User is not an operator")


def disapprove_request(id, request_id):
    user = get_user(id)
    if user.user_type == User.OPERATOR:
        request = get_user_request(request_id)
        if request.evaluated:
            raise BadRequest("Request already evaluated")
        user = request.disapprove()
        return user
    else:
        raise Unauthorized("User is not an operator")


def get_user_request(id):
    request = UserCreationRequest.query.get(id)
    return request


def get_all_user_requests():
    return UserCreationRequest.query.all()


def get_unevaluated_user_requests():
    return UserCreationRequest.query.filter_by(evaluated=False).all()


def get_all():
    return User.query.all()


def get_user(id):
    user = User.query.get(id)
    if user is None: raise NotFound(f"User with id {id} was not found")
    return user


def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user is None: raise NotFound(f"User with email {email} was not found")
    return user


def forget_user(id):
    user = get_user(id)
    user.be_forgotten()
    return user


def check_is_operator(id):
    user = get_user(id)
    if user.user_type != User.OPERATOR:
        raise Unauthorized("User is not an operator")


def check_password(email, password):
    u = get_user_by_email(email)
    return password == u.password


def add_image(id, image, data=None):
    u = get_user(id)
    if u.user_type == User.OPERATOR:
        id = data.get('id')
    u.add_image(image)
    return u


def update_user(id, data):
    u = get_user(id)
    u.update(data)
    return u


def add_interaction(requester_id, id, data):
    requester = get_user(requester_id)
    if requester.user_type == User.OPERATOR:
        user = get_user(id)
        return user.add_interaction(data.get('interaction_type'), data.get('detail'))
    raise Unauthorized("User is not an operator")
