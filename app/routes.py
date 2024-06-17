import os
from flask import current_app, render_template, flash, redirect, url_for, request, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User, Book, Review, Genre, Role, Cover
from app.forms import LoginForm, RegistrationForm, BookForm, ReviewForm, RoleAssignmentForm
from functools import wraps

bp = Blueprint('main', __name__)

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role.name not in roles:
                if not current_user.is_authenticated:
                    return redirect(url_for('main.login', next=request.url))
                else:
                    flash('У вас недостаточно прав для выполнения данного действия.')
                    return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    books = Book.query.order_by(Book.year.desc()).paginate(page=page, per_page=10, error_out=False)

    next_url = url_for('main.index', page=books.next_num) if books.has_next else None
    prev_url = url_for('main.index', page=books.prev_num) if books.has_prev else None

    return render_template('index.html', title='Home', books=books.items, next_url=next_url, prev_url=prev_url)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/add_book', methods=['GET', 'POST'])
@login_required
@role_required('Администратор')
def add_book():
    form = BookForm()
    form.genres.choices = [(g.id, g.name) for g in Genre.query.all()]
    form.cover_id.choices = [(c.id, c.file_name) for c in Cover.query.all()]

    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            description=form.description.data,
            year=form.year.data,
            publisher=form.publisher.data,
            author=form.author.data,
            pages=form.pages.data,
            cover_id=form.cover_id.data
        )
        selected_genres = Genre.query.filter(Genre.id.in_(form.genres.data)).all()
        book.genres.extend(selected_genres)
        db.session.add(book)
        db.session.commit()
        flash('Book has been added!')
        return redirect(url_for('main.index'))
    return render_template('add_book.html', title='Add Book', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, 
                    last_name=form.last_name.data,
                    first_name=form.first_name.data,
                    middle_name=form.middle_name.data,
                    role_id=3)  # По умолчанию роль "Пользователь"
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/add_review/<int:book_id>', methods=['GET', 'POST'])
@login_required
@role_required('Пользователь')
def add_review(book_id):
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(book_id=book_id, user_id=current_user.id, rating=form.rating.data, review_text=form.review_text.data)
        db.session.add(review)
        db.session.commit()
        flash('Your review has been added!')
        return redirect(url_for('main.book_detail', id=book_id))
    return render_template('add_review.html', title='Add Review', form=form)

@bp.route('/assign_role', methods=['GET', 'POST'])
@login_required
@role_required('Администратор')
def assign_role():
    form = RoleAssignmentForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            user.role_id = form.role.data
            db.session.commit()
            flash('Role has been assigned!')
        else:
            flash('User not found.')
        return redirect(url_for('main.index'))
    return render_template('assign_role.html', title='Assign Role', form=form)

@bp.route('/edit_book/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('Администратор', 'Модератор')
def edit_book(id):
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    form.genres.choices = [(g.id, g.name) for g in Genre.query.all()]
    form.cover_id.choices = [(c.id, c.file_name) for c in Cover.query.all()]

    if form.validate_on_submit():
        book.title = form.title.data
        book.description = form.description.data
        book.year = form.year.data
        book.publisher = form.publisher.data
        book.author = form.author.data
        book.pages = form.pages.data
        book.cover_id = form.cover_id.data
        book.genres = Genre.query.filter(Genre.id.in_(form.genres.data)).all()
        db.session.commit()
        flash('Book has been updated!')
        return redirect(url_for('main.index'))
    return render_template('edit_book.html', title='Edit Book', form=form, book=book)

@bp.route('/delete_book/<int:id>', methods=['POST'])
@login_required
@role_required('Администратор')
def delete_book(id):
    book = Book.query.get_or_404(id)
    cover_path = os.path.join(current_app.root_path, 'static', 'covers', book.cover.file_name)

    # Удаление книги и всех связанных записей
    db.session.delete(book)
    db.session.commit()

    # Удаление файла обложки
    if os.path.exists(cover_path):
        os.remove(cover_path)

    flash('Book has been deleted!')
    return redirect(url_for('main.index'))

@bp.route('/book/<int:id>')
def book_detail(id):
    book = Book.query.get_or_404(id)
    reviews = Review.query.filter_by(book_id=book.id).all()
    return render_template('book_detail.html', title=book.title, book=book, reviews=reviews)
