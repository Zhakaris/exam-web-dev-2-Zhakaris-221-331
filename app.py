from flask import Flask, render_template, redirect, url_for, flash, request, session
from werkzeug.utils import secure_filename
from models import db, Book, Cover, Genre, BookGenre, User
from forms import BookForm
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://std_2419_zhak_project:zhakaris@std-mysql.ist.mospolytech.ru/std_2419_zhak_project'
app.config['SECRET_KEY'] = 'b3baa1cb519a5651c472d1afa1b3f4e04f1adf6909dae88a4cd39adc0ddd9732'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db.init_app(app)

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    books = Book.query.order_by(Book.year.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', books=books)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session['user_id'] = user.id
            session['role'] = user.role.name
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book_id).all()
    return render_template('book_detail.html', book=book, reviews=reviews)

@app.route('/book/add', methods=['GET', 'POST'])
def add_book_view():
    if 'user_id' not in session:
        flash('Для выполнения данного действия необходимо пройти процедуру аутентификации', 'danger')
        return redirect(url_for('login'))
    if session.get('role') != 'Администратор':
        flash('У вас недостаточно прав для выполнения данного действия', 'danger')
        return redirect(url_for('index'))
    
    form = BookForm()
    if form.validate_on_submit():
        # Save the cover image
        file = form.cover.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Compute MD5 hash
        md5_hash = 'dummy_hash'  # Replace with actual hash calculation
        
        # Create cover record
        cover = Cover(file_name=filename, mime_type=file.mimetype, md5_hash=md5_hash)
        db.session.add(cover)
        db.session.commit()

        # Create book record
        book = Book(
            title=form.title.data,
            description=form.description.data,
            year=form.year.data,
            publisher=form.publisher.data,
            author=form.author.data,
            pages=form.pages.data,
            cover_id=cover.id
        )
        db.session.add(book)
        db.session.commit()

        # Add genres to book
        for genre_id in form.genres.data:
            book_genre = BookGenre(book_id=book.id, genre_id=genre_id)
            db.session.add(book_genre)
        
        db.session.commit()

        flash('Book added successfully.', 'success')
        return redirect(url_for('index'))
    return render_template('add_book.html', form=form)


@app.route('/book/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book_view(book_id):
    if 'user_id' not in session:
        flash('Для выполнения данного действия необходимо пройти процедуру аутентификации', 'danger')
        return redirect(url_for('login'))
    if session.get('role') not in ['Администратор', 'Модератор']:
        flash('У вас недостаточно прав для выполнения данного действия', 'danger')
        return redirect(url_for('index'))
    
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        form.populate_obj(book)
        db.session.commit()
        flash('Book updated successfully.', 'success')
        return redirect(url_for('index'))
    return render_template('edit_book.html', form=form, book_id=book_id)


@app.route('/book/delete/<int:book_id>', methods=['POST'])
def delete_book_view(book_id):
    if 'user_id' not in session:
        flash('Для выполнения данного действия необходимо пройти процедуру аутентификации', 'danger')
        return redirect(url_for('login'))
    if session.get('role') != 'Администратор':
        flash('У вас недостаточно прав для выполнения данного действия', 'danger')
        return redirect(url_for('index'))
    
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully.', 'success')
    return redirect(url_for('index'))


@app.route('/review/add/<int:book_id>', methods=['GET', 'POST'])
def add_review_view(book_id):
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(book_id=book_id, user_id=session['user_id'], rating=form.rating.data, review_text=form.review_text.data)
        db.session.add(review)
        db.session.commit()
        flash('Review added successfully.', 'success')
        return redirect(url_for('book_detail', book_id=book_id))
    return render_template('review_form.html', form=form, book_id=book_id)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
