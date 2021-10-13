from db import db
from flask_restful import fields
from abc import ABCMeta


class BaseModel(db.Model):
    __metaclass__ = ABCMeta
    __abstract__ = True

    def save(self):
        db.session.add(self)
        db.session.commit()


class UserCreationRequest(BaseModel):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    professional_email = db.Column(db.String(80))
    professional_title = db.Column(db.String(80))
    user_type = db.Column(db.Integer, nullable=False)
    evaluated = db.Column(db.Boolean, nullable=False, default=False)
    images = db.Column(db.PickleType)

    api_fields = {
        "id": fields.Integer,
        "email": fields.String,
        "user_type": fields.Integer,
        "evaluated": fields.Boolean,
        "phone": fields.String,
        "professional_email": fields.String,
        "professional_title": fields.String,
        "address": fields.String
    }

    def _convert_user_image(self):
        if len(self.images) > 0:
            image = UserImage.query.get(self.images[0])
            return [image]
        else:
            return []


    def approve(self):
        self.evaluated = True

        images = self._convert_user_image()

        user = User(email=self.email, password=self.password, user_type=self.user_type, address=self.address,
                    phone=self.phone, professional_email=self.professional_email, professional_title=self.professional_title, images=images)

        if len(self.images) > 0:
            image = images[0]
            image.user_id = user.id
            image.user = user

        user.save()
        self.save()
        return user

    def disapprove(self):
        self.evaluated = True
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()




class UserImage(BaseModel):

    USER_PROVIDED = 1
    CAMERA_CAPTURED = 2

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary(length=(2**32)-1), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=user_id)
    image_type = db.Column(db.Integer, nullable=False, default=USER_PROVIDED)
    temperature = db.Column(db.Float, nullable=True)

    api_fields = {
        "id": fields.Integer,
        "image": fields.String,
        "temperature": fields.Float
    }

    def __getattribute__(self, name):
        if name == "image":
            return super().__getattribute__(name).decode()
        return super().__getattribute__(name)


class Interaction(BaseModel):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=user_id)
    detail = db.Column(db.PickleType)
    interaction_type = db.Column(db.Integer)

    api_fields = {
        "id": fields.Integer,
        "user": fields.Integer(attribute="user_id")
    }


class User(BaseModel):

    COMMUNITY_MEMBER = 1
    OPERATOR = 2

    NOT_UPDATEABLE = ["id", "images", "email", "password"]

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    forgotten = db.Column(db.Boolean, nullable=False, default=False)
    user_type = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    professional_email = db.Column(db.String(80))
    professional_title = db.Column(db.String(80))
    images = db.relationship('UserImage')
    interactions = db.relationship('Interaction')

    api_fields = {
        "id": fields.Integer,
        "email": fields.String,
        "images": fields.Nested(UserImage.api_fields),
        "phone": fields.String,
        "professional_email": fields.String,
        "professional_title": fields.String,
        "address": fields.String,
        "interactions": fields.Nested(Interaction.api_fields)
    }

    def add_image(self, image):
        image = UserImage(user_id=self.id, user=self, image=image.encode())
        self.images.append(image)
        image.save()
        self.save()
        return image

    def add_interaction(self, interaction_type, detail):
        interaction = Interaction(interaction_type=interaction_type, detail=detail)
        self.interactions.append(interaction)
        interaction.save()
        self.save()
        return interaction

    def update(self, data):
        for attr in data.keys():
            if attr not in self.NOT_UPDATEABLE:
                self.__setattr__(attr, data[attr])
        self.save()



class PasswordResetRequest(BaseModel):

    token = db.Column(db.String(32), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', foreign_keys=user_id)
