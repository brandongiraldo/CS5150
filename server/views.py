from flask import render_template, flash, redirect
from server import app
from .forms import LoginForm

from flask import request
from flask import render_template_string
from models import Post, Student, Professor


@app.route('/')
@app.route('/index')
@app.route('/posts')
@app.route('/posts/')
@app.route('/posts/tags=<tags>')
@app.route('/posts/tags=<tags>/<all>')
def index(tags=None, all=None):
    user = {'nickname': 'Michael'}
    if tags:
        tags = tags.lower().strip().split(',')
    posts = Post.get_posts(tags=tags, exclusive=True if all == 'all' else False)
    return render_template(
        "index.html",
        title='Home',
        user=user,
        posts=posts,
        search=True,
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for User="%s", remember_me=%s' %
              (form.username.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template(
        'login.html',
        title='Sign In',
        form=form
    )


@app.route('/profile/<net_id>', methods=['GET'])
def profile(net_id):
    user = Student.get_student_by_netid(net_id)
    # return render_template_string('hello {{ id }}', id=user.name)
    user.email = user.net_id + "@cornell.edu"
    user.major = "Computer Science"
    user.year = "Junior"
    user.skills = ["Java", "C++", "Python"]
    user.resume = "resume.pdf"
    user.description = "I'm a Junior in Computer Science who is interested in algorithms research. I worked at Mircosoft Research this past summer."
    user.interests = ["Algorithms", "Data Science", "Research"]
    user.favorited_projects = ["Copy Cats", "Algorithmic Game Theory", "Smash AI"]
    user.availability = ["Mon", "Wed", "Fri"]

    return render_template(
      'profile.html',
      title=user.name + "'s Profile",
      profile=user,
    )


@app.route('/posts/create', methods=['GET', 'POST'])
def createpost():
    if request.method == 'POST':
        result = request.form
        Post.create_post(
            result["title"], result["description"], "professor_id", "tags", "qualifications",
            "current_students", "desired_skills",
            "capacity", "current_number"
        )
        return redirect("/posts", code=302)
    else:
        return render_template(
            'createpost.html',
            title='Sign In'
        )


@app.route('/posts/<int:post_id>', methods=['GET'])
def showpost(post_id):
    post = Post.get_post_by_id(post_id)
    return render_template(
        'post.html',
        post=post
    )


@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
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
