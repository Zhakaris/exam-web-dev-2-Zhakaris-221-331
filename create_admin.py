# create_admin.py
from app import app, db
from models import User, Role
from werkzeug.security import generate_password_hash

def create_admin():
    with app.app_context():
        admin_role = Role.query.filter_by(name='Администратор').first()
        if not admin_role:
            print("Роль 'Администратор' не найдена. Пожалуйста, сначала выполните create_roles.py.")
            return

        admin_user = User(
            username='Zhakaris_admin',
            password_hash=generate_password_hash('zhakaris'),
            first_name='Zhakaris',
            last_name='Admin',
            role_id=admin_role.id
        )

        db.session.add(admin_user)
        db.session.commit()
        print("Пользователь 'zhakaris' с ролью 'Администратор' успешно создан.")

if __name__ == '__main__':
    create_admin()
