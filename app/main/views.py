import os  # helps grab the file extension ie .jpg /png from the uploaded images
import secrets  # used to create a random hex to randomize the name of the p.pics to avoid conflicts
# this helps in shrinking down/resizing large images to save space on the database
from PIL import Image
from flask import render_template, request, redirect, url_for, abort, flash, current_app
from . import main
# import markdown2
from ..models import User, Post
from .. import db, photos
from flask_login import login_required, current_user
from .forms import UpdateAccountForm, PostForm
from ..requests import get_quote


@main.route('/')
@main.route('/home')
def index():
    # grabs the page number from the url
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(
        page=page, per_page=5)  # this sets the max number of posts per page to 5
    quote_object = get_quote()
    # author= quote_object["author"]
    quote = quote_object["quote"]
    print(quote)
    # posts=Post.query.all()  #this fetches all the posts  use pagination to limit the number of posts per page for neatness and curiosity
    title = "devgarage"
    return render_template("index.html", title=title, posts=posts)


@main.route('/about')
def about():
    title = 'about'
    return render_template("about.html", title=title)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    # function to split the filename from the file extension...underscores are used in place of a variable you wont use in order to avoid errors
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext  # to create the new random filename and extension
    # this joins everything to form a valid path to where the images will be stored
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics', picture_fn)

    # output_size = (125, 125)
    i = Image.open(form_picture)
    # i.thumbnail(output_size)
    i.save(picture_path)  # this actually saves the picture to the path

    return picture_fn  # returns the new random file name


@main.route('/account', methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            # this should be able to update the users p.picture
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        flash("Youre credentials have been updated successfullly!!")
        return redirect(url_for('main.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    title = "my account"
    return render_template("account.html", title=title, image_file=image_file, form=form)


@main.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!')
        return redirect(url_for('main.index'))
    return render_template('create_post.html', title='New Post', form=form, heading='New Post')


# will deal with showing a template with all the users own posts

@main.route('/user/<string:username>')
def user_posts(username):
    # grabs the page number from the url
    page = request.args.get('page', 1, type=int)

    # ie get the first user with said username or else display a 404 error
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)  # this sets the max number of posts per page to 5

    # posts=Post.query.all()  #this fetches all the posts  use pagination to limit the number of posts per page for neatness and curiosity
    title = " user posts"
    return render_template("user_posts.html", title=title, posts=posts, user=user)


@main.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@main.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # 403 error means that route is forbidden
    form = PostForm()
    if form.validate_on_submit():
        # this captures the new update on the title and the content..and over writes the existing data
        post.title = form.title.data
        # also because we are updating we dont need the db.session.add('') because the info is already in the db
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')

        return redirect(url_for('main.post', post_id=post.id))

    elif request.method == 'GET':  # this tells the app to fetch the original data that the post has .no alterations made
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title='Update Post',
                           form=form, heading='Update Post')


@main.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!')
    return redirect(url_for('main.index'))
