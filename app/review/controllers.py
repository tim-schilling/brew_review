from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from app import db
from .forms import ReviewForm, BrewForm
from .models import Brew, Review

review_blueprint = Blueprint('review', __name__, url_prefix='')


@review_blueprint.route('/')
def index():
    brews = Brew.query.all()
    return render_template('index.html', brews=brews)


@review_blueprint.route('/<brew_slug>/')
def view_brew(brew_slug):
    brew = Brew.query.filter_by(slug=brew_slug).first_or_404()
    reviews = brew.reviews
    return render_template('review/brew.html', brew=brew, reviews=reviews)


@review_blueprint.route('/create/', methods=['GET', 'POST'])
def create_brew():
    form = BrewForm(request.form)
    brew = None
    if form.validate_on_submit():
        brew = form.populate(Brew())
        db.session.add(brew)
        db.session.commit()
        flash('You have created a brew.')
        return redirect(url_for('.view_brew', brew_slug=brew.slug))
    return render_template('review/create_brew.html', form=form, brew=brew)


@review_blueprint.route('/<brew_slug>/review/', methods=['GET', 'POST'])
def review_brew(brew_slug):
    brew = Brew.query.filter_by(slug=brew_slug).first_or_404()
    form = ReviewForm(request.form)
    review = None
    if form.validate_on_submit():
        review = form.populate(Review())
        review.brew_id = brew.id
        db.session.add(review)
        db.session.commit()
        flash('You have reviewed a brew.')
        return redirect(url_for('.view_brew', brew_slug=brew.slug))
    return render_template(
        'review/review_brew.html',
        form=form, brew=brew, review=review, MAX_SCORES=Review.MAX_SCORES)
