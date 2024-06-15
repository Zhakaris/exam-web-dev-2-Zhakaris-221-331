# create_roles.py
from app import app, db
from models import Role

def create_roles():
    with app.app_context():
        admin_role = Role(name='Администратор', description='Суперпользователь, имеет полный доступ к системе')
        user_role = Role(name='Пользователь', description='Может оставлять рецензии')
        moderator_role = Role(name='Модератор', description='Может редактировать данные книг и производить модерацию рецензий')

        db.session.add(admin_role)
        db.session.add(user_role)
        db.session.add(moderator_role)
        db.session.commit()

if __name__ == '__main__':
    create_roles()
