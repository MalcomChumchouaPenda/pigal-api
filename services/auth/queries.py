from core.config import db
from .schemas import User, Role


def init_users():
    if not Role.query.first():
        roles = [
            Role(id='admin', name='Admin'),
            Role(id='teacher', name='Teacher'),
            Role(id='user', name='User')
        ]
        db.session.add_all(roles)
        db.session.commit()
    
    if not User.query.first():
        users_data = [
            dict(id='admin1', pwd='adminpass', role='admin'),
            dict(id='teacher1', pwd='teacherpass', role='teacher'),
            dict(id='user1', pwd='userpass', role='user'),
        ]
        for row in users_data:
            role = Role.query.filter_by(id=row['role']).one()
            user = User(id=row['id'], roles=[role])
            user.set_password(row['pwd'])
            db.session.add(user)
        db.session.commit()


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
