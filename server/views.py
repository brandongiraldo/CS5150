from flask import render_template, flash, redirect, request
from server import app
from .forms import LoginForm
from flask_login import login_user, logout_user, login_required
from flask import render_template_string
from models import Post, Student, Professor


@app.route('/')
@app.route('/index')
@app.route('/posts')
@app.route('/posts/')
@app.route('/posts/tags=<tags>')
@app.route('/posts/tags=<tags>/<all>')
# I need to know the netid of the student here so I can get back the
# favorited_projects for them on the search / home page.
@login_required
def index(tags=None, all=None):
    user = {'nickname': 'Michael'}
    if tags:
        tags = tags.lower().strip().split(',')
    posts = Post.get_compressed_posts(tags=tags, exclusive=True if
                                      all == 'all' else False)
    return render_template(
        "index.html",
        title='Home',
        user=user,
        posts=posts,
        search=True,
        isInIndex=True
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = (Professor.query.filter_by(email=form.email.data).first() or
                Student.query.filter_by(email=form.email.data).first())
        if user:
            if user.is_correct_password(form.password.data):
                login_user(user)
                flash('Welcome back %s!' % user.name)
                next = request.args.get('next')
                return redirect(next or '/index')
            else:
                return redirect('/login')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/index')


@app.route('/profile/<net_id>', methods=['GET', 'POST'])
@login_required
def profile(net_id):
    user = Student.get_student_by_netid(net_id)
    favorited_projects = Student.get_student_favorited_projects(net_id)
    if request.method == 'POST':
        result = request.form
        new_email = result["user_email"] or (net_id + "@cornell.edu")
        new_year = result["user_year"] or "Freshman"
        new_description = result["user_description"] or " "
        interests = result["interests"]
        skills = result["skills"]
        availability = ','.join(result.getlist("weekday"))
        # Flask fileupload ?
        resume = result["resume"]
        user = Student.update_student(
            net_id, email=new_email, name=None, major=user.major, year=new_year,
            skills=skills, resume=resume, description=new_description,
            interests=interests, favorited_projects=None, availability=availability
        )
        return redirect("/profile/" + net_id, code=302)
    else:
        return render_template(
          'profile.html',
          title=user.name + "'s Profile",
          profile=user,
          favorited_projects=favorited_projects,
          current_user=user
        )


@app.route('/posts/create', methods=['GET', 'POST'])
@login_required
def createpost():
    if request.method == 'POST':
        result = request.form
        Post.create_post(
            result["post_title"], result["post_description"], "professor_id",
            "tags", "qualifications", "current_students", "desired_skills",
            "capacity", "current_number"
        )
        return redirect("/posts", code=302)
    else:
        return render_template(
            'createpost.html',
            title='Sign In'
        )


@app.route('/posts/<int:post_id>', methods=['GET'])
@login_required
def showpost(post_id):
    post = Post.get_post_by_id(post_id)
    return render_template(
        'post.html',
        post=post
    )


@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def editpost(post_id):
    if request.method == 'POST':
        result = request.form
        return render_template_string(
            "{{ result.title }} result {{ result.description }}",
            result=result
        )
    else:
        return render_template(
            'createpost.html',
            id='Sign In'
        )


@app.route('/styleguide', methods=['GET'])
def get_styleguide():
    return render_template(
        'styleguide.html'
    )
