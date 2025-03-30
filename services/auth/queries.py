
from core.config import db
from .schemas import User, Role


def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id)

def get_user_by_role(role_name):
    return User.query.join(User.roles).filter(Role.name == role_name).all()

def create_user(user_id, password, role_id):
    user = User(id=user_id)
    user.set_password(password)
    role = Role.query.filter_by(id=role_id)
    if role:
        user.roles.append(role)
    db.session.add(user)
    db.session.commit()
    return user

def delete_user(user_id):
    user = User.query.filter_by(id=user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

def update_user_password(user_id, new_password):
    user = User.query.filter_by(id=user_id)
    if user:
        user.set_password(new_password)
        db.session.commit()
        return True
    return False
