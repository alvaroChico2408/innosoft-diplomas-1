from app import db
import os
from app.modules.auth.utils import remove_existing_file, get_unique_filename
from werkzeug.exceptions import InternalServerError


'''
class UserProfile(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
'''
class UserProfile(db.Model):
    """
    A User profile model class.
    """

    __tablename__ = "user_profile"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(200), default="")
    surname = db.Column(db.String(100), nullable=False)
    avator = db.Column(db.String(250), default="")

    user = db.relationship("User", backref="profile", foreign_keys=[user_id])
    #user = db.relationship("User", foreign_keys=[user_id])


    def save(self):
            db.session.add(self)
            db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        

    def set_avator(self, profile_image):
        """
        Set a new avatar for the user by removing the existing avatar (if any), saving the new one,
        and updating the user's avatar field in the database.

        :param profile_image: The uploaded image file to be set as the new avatar.

        :raises InternalServerError: If there is an error during the file-saving process.
        """
        from config import UPLOAD_FOLDER

        if self.avator:
            path = os.path.join(UPLOAD_FOLDER, self.avator)
            remove_existing_file(path=path)

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(os.path.join(UPLOAD_FOLDER), exist_ok=True)

        self.avator = get_unique_filename(profile_image.filename)

        try:
            # Save the new avatar file to the file storage.
            profile_image.save(os.path.join(UPLOAD_FOLDER, self.avator))
        except Exception as e:
            # Handle exceptions that might occur during file saving.
            print("Error saving avatar: %s" % e)
            raise InternalServerError

    def __repr__(self):
        return "<Profile '{}'>".format(self.user.username)