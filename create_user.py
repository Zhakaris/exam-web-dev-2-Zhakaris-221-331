from werkzeug.security import generate_password_hash
from app import app, db
from models import User, Role

def create_user(username, password, first_name, last_name, role_name):
    with app.app_context():
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            print(f"Role '{role_name}' not found.")
            return

        hashed_password = generate_password_hash(password)
        user = User(username=username, password_hash=hashed_password, first_name=first_name, last_name=last_name, role_id=role.id)
        db.session.add(user)
        db.session.commit()
        print(f"User '{username}' created successfully.")

if __name__ == '__main__':
    create_user('Zhakaris', 'zhakaris', 'Zhakaris', 'Margaria', 'Пользователь')
