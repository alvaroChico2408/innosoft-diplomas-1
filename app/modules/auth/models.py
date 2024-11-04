from datetime import datetime, timedelta


from flask_login import UserMixin
from app.modules.auth.utils import unique_security_token
from werkzeug.exceptions import InternalServerError, HTTPException
import typing as t
from sqlalchemy import Index, or_
#import pytz
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

'''
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(256), unique=True, nullable=True)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(pytz.utc))

    profile = db.relationship('UserProfile', backref='user', uselist=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if 'password' in kwargs:
            self.set_password(kwargs['password'])

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def temp_folder(self) -> str:
        from app.modules.auth.services import AuthenticationService
        return AuthenticationService().temp_folder_by_user(self)

'''
class User(db.Model, UserMixin):
    """
    A Base User model class.
    """

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    profile = db.relationship('UserProfile', backref='user', uselist=False)
    active = db.Column(db.Boolean, default=False, nullable=False, server_default="0")
    change_email = db.Column(db.String(120), default="")
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


    def save(self):
            db.session.add(self)
            db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        

    @classmethod
    def authenticate(
        cls, username: t.AnyStr = None, password: t.AnyStr = None
    ) -> t.Optional["User"]:
        """
        Authenticates a user based on their username or email and password.

        :param username: The username or email of the user attempting to authenticate.
        :param password: The password of the user attempting to authenticate.

        :return: The authenticated user object if credentials are correct, otherwise None.
        """
        user = cls.query.filter(
            or_(
                cls.username == username,
                cls.email == username,
            )
        ).first()

        if user and user.check_password(password):
            return user

        return None

    @classmethod
    def create(cls, **kwargs):
        """
        Create a new user instance, set the password,
        and save it to the database.

        :return: The newly created user instance.

        :raises InternalServerError: If there is an error while creating or saving the user.
        """
        password = kwargs.get("password")

        try:
            user = cls(**kwargs)
            user.set_password(password)
            user.save()
        except Exception as e:
            # Handle database error by raising an internal server error.
            raise InternalServerError

        return user

    @classmethod
    def get_user_by_id(cls, user_id: t.AnyStr, raise_exception: bool = False):
        """
        Retrieves a user instance from the database
        based on their User ID.

        :param user_id: The ID of the user to retrieve instance.
        """
        if raise_exception:
            return cls.query.get_or_404(user_id)

        return cls.query.get(user_id)

    @classmethod
    def get_user_by_username(cls, username: t.AnyStr):
        """
        Retrieves a user instance from the database
        based on their username.

        :param username: The username of the user to retrieve.
        """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_email(cls, email: t.AnyStr):
        """
        Retrieves a user instance from the database
        based on their email address.

        :param email: The email address of the user to retrieve.
        """
        return cls.query.filter_by(email=email).first()

    def set_password(self, password: t.AnyStr):
        """
        Sets the password for the user after hashing it.

        :param password: The plain-text password to hash and set.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password: t.AnyStr) -> bool:
        """
        Checks if the provided password matches the hashed password.

        :param password: The plain-text password to check.
        """
        return check_password_hash(self.password, password)

    def generate_token(self, salt: str) -> t.AnyStr:
        """
        Generates a new security token for the user.

        :return: The newly created security token.
        """
        instance = UserSecurityToken.create_new(salt=salt, user_id=self.id)
        return instance.token

    @staticmethod
    def verify_token(
        token: t.AnyStr, salt: str, raise_exception: bool = True
    ) -> t.Union[t.Optional["UserSecurityToken"], HTTPException, None]:
        """
        Verifies whether a security token is valid and not expired.

        :param token: The security token to verify.
        :param raise_exception: If True, raises a 404 error if the token is not found. Defaults to True.

        :return: `True` if the token exists and is not expired, `False` otherwise.
        """
        instance = UserSecurityToken.query.filter_by(token=token, salt=salt)

        if raise_exception:
            token = instance.first_or_404()
        else:
            token = instance.first()

        if token and not token.is_expired:
            return token

        return None

    
    def send_confirmation(self):
        """
        Sends user's account confirmation email.
        """
        from app.modules.confirmemail.utils import send_confirmation_mail

        send_confirmation_mail(self)
    

    @property
    def is_active(self) -> bool:
        """
        Checks if the user's account is active.

        :return: `True` if the user account is active, otherwise `False`.
        """
        return self.active

    def __repr__(self):
        return "<User '{}'>".format(self.username)
    
    
class UserSecurityToken(db.Model):
    """
    A token class for storing security token for url.
    """

    __tablename__ = "user_token"

    id = db.Column(db.Integer, primary_key=True)

    __table_args__ = (
        Index("ix_user_token_token", "token"),
        Index("ix_user_token_expire", "expire"),
    )

    token = db.Column(
        db.String(72), default=unique_security_token, nullable=False, unique=True
    )

    salt = db.Column(db.String(20), nullable=False)

    expire = db.Column(db.Boolean, default=False, nullable=False, server_default="0")

    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    user = db.relationship("User", foreign_keys=[user_id])


    def save(self):
            db.session.add(self)
            db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        

    @classmethod
    def create_new(cls, **kwargs) -> t.AnyStr:
        """
        Creates a new security token instance for a user
        and saves it to the database.

        :param user_id: The ID of the user for whom the token is being created.
        :return: The generated security token string.

        :raises InternalServerError: If there is an error saving the token to the database.
        """
        try:
            instance = cls(**kwargs)
            instance.save()
        except Exception as e:
            raise InternalServerError

        return instance

    @property
    def is_expired(self) -> bool:
        """
        Checks if the token has expired based
        on its creation time and expiration period.
        """
        if not self.expire:
            expiry_time = self.created_at + timedelta(minutes=15)
            current_time = datetime.now()

            if not expiry_time <= current_time:
                return False

        self.delete()
        return True

    @classmethod
    def is_exists(cls, token: t.AnyStr = None):
        """
        Check if a token already exists in the database.

        :param token: The token to check for existence.

        :return: The first instance found with the specified token,
        or None if not found.
        """
        return cls.query.filter_by(token=token).first()

    def __repr__(self):
        return "<Token '{}' by {}>".format(self.token, self.user)