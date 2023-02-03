from db import db


class RoleModel(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    users = db.relationship(
        "UserModel", back_populates="roles", secondary="users_roles")

    @staticmethod
    def get_by_name(name):
        return RoleModel.query.filter_by(name=name).first()
