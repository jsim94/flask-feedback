from flask import Flask, render_template, flash, redirect, session, abort
from models import db, connect_db, User, Feedback
from forms import RegisterUser, Login, FeedbackForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ajhkgijtr54y67w334tasedfgcjhv'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

######################################
# home routes
######################################


@app.route('/')
def home_route():
    return redirect('/users')


@app.route('/users')
def show_all_users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUser()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username=username, password=password,
                             email=email, first_name=first_name, last_name=last_name)

        db.session.add(user)
        db.session.commit()
        session['username'] = user.username

        return redirect('/users')
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username=username, password=password)

        if user:
            session['username'] = user.username
            return redirect('/users')
        else:
            flash('Incorrect username or password')
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

######################################
# user routes
######################################


@app.route('/users/<username>')
def show_user(username):
    if not session.get('username'):
        return redirect('/login')

    user = User.query.get_or_404(username)

    if not user.username == session.get('username'):
        abort(401)

    return render_template('user.html', user=user)


@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    if not session.get('username'):
        return redirect('/login')

    user = User.query.get_or_404(username)

    if not user.username == session.get('username'):
        abort(401)

    user.delete()
    session.clear()
    return redirect('/users')

######################################
# feedback routes
######################################


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def new_feedback(username):
    if not session.get('username'):
        return redirect('/login')

    form = FeedbackForm()

    if form.validate_on_submit():
        if not username == session.get('username'):
            abort(401)

        title = form.title.data
        content = form.content.data
        user = User.query.get(username)

        feedback = Feedback(
            title=title, content=content, username=username, user=user)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f'/users/{username}')
    else:
        return render_template('feedback-form.html', form=form)


@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    if not session.get('username'):
        return redirect('/login')

    feedback = Feedback.query.get_or_404(feedback_id)

    form = FeedbackForm()

    if form.validate_on_submit():
        if not feedback.username == session.get('username'):
            abort(403)

        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.add(feedback)
        db.session.commit()

        return redirect(f'/users/{feedback.username}')
    else:
        return render_template('feedback-form.html', form=form)


@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    user = session.get('username')

    if not user:
        return redirect('/login')

    feedback = Feedback.query.get_or_404(feedback_id)

    if not feedback.username == user:
        abort(401)

    feedback.delete()
    return redirect(f'/users/{user}')
