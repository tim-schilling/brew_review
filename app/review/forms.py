from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SelectField, DateField, FloatField
from wtforms.validators import DataRequired, Email, NumberRange, Optional
from wtforms.widgets import TextArea

from .models import STYLES, Review


class BrewForm(Form):
    name = StringField('Brew Name', [DataRequired()])
    brewer = StringField('Your Name', [DataRequired()])
    email = StringField('Your Email', [Email(), Optional()])
    style = SelectField('Style', choices=STYLES, validators=[DataRequired()])
    brewed = DateField('Brew Date', [Optional()], format='%m-%d-%Y')
    bottled = DateField('Bottling Date', [Optional()], format='%m-%d-%Y')
    og = FloatField('Original Gravity', [Optional(), NumberRange(.9, 2.0)])
    fg = FloatField('Final Gravity', [Optional(), NumberRange(.9, 2.0)])
    fermentables = StringField(
        'Fermentables', [Optional()], widget=TextArea(),
        description="List of fermentables: name, weights.")
    mash_schedule = StringField('Mash Schedule', [Optional()], widget=TextArea())
    hops = StringField(
        'Hops', [Optional()], widget=TextArea(),
        description="List of hops: name, usage (boil, flameout, dry-hop) and "
                    "duration.")
    yeast = StringField('Yeast', [Optional()])
    comments = StringField(
        'Extra Information', [Optional()], widget=TextArea(),
        description="Additional comments and/or special ingredients.")

    def populate(self, obj):
        obj.name = self.data.get('name')
        obj.brewer = self.data.get('brewer')
        obj.slug = obj.find_slug(obj.name, obj.brewer)
        obj.email = self.data.get('email')
        obj.style = self.data.get('style')
        obj.brewed = self.data.get('brewed')
        obj.bottled = self.data.get('bottled')
        obj.og = self.data.get('og')
        obj.fg = self.data.get('fg')
        obj.fermentables = self.data.get('fermentables')
        obj.mash_schedule = self.data.get('mash_schedule')
        obj.hops = self.data.get('hops')
        obj.yeast = self.data.get('yeast')
        obj.comments = self.data.get('comments')
        return obj


class ReviewForm(Form):
    name = StringField('Your Name', [Optional()])
    aroma_score = IntegerField('Aroma Score', [
        DataRequired(), NumberRange(0, Review.MAX_SCORES['aroma_score'])])
    aroma_comments = StringField(
        'Aroma Comments', [Optional()], widget=TextArea(),
        description="Comment on malt, hops, esters, and other aromatics."
    )
    appearance_score = IntegerField('Appearance Score', [
        DataRequired(), NumberRange(0, Review.MAX_SCORES['appearance_score'])])
    appearance_comments = StringField(
        'Appearance Comments', [Optional()], widget=TextArea(),
        description="Comment on color, clarity, and head (retention, color, "
                    "and texture)."
    )
    flavor_score = IntegerField('Flavor Score', [
        DataRequired(), NumberRange(0, Review.MAX_SCORES['flavor_score'])])
    flavor_comments = StringField(
        'Flavor Comments', [Optional()], widget=TextArea(),
        description="Comment on malt, hops, fermentation characteristics, "
                    "balance, finish/aftertaste, and other flavor "
                    "characteristics."
    )
    mouthfeel_score = IntegerField('Mouthfeel Score', [
        DataRequired(), NumberRange(0, Review.MAX_SCORES['mouthfeel_score'])])
    mouthfeel_comments = StringField(
        'Mouthfeel Comments', [Optional()], widget=TextArea(),
        description="Comment on body, carbonation, warmth, creaminess, "
                    "astringency, and other palate sensations."
    )
    impression_score = IntegerField('Overall Impression Score', [
        DataRequired(), NumberRange(0, Review.MAX_SCORES['impression_score'])])
    impression_comments = StringField(
        'Overall Impression Comments', [Optional()], widget=TextArea(),
        description="Comment on overall drinking pleasure associated with "
                    "entry, give suggestions for improvement."
    )

    def populate(self, obj):
        obj.name = self.data.get('name')
        obj.aroma_score = self.data.get('aroma_score')
        obj.aroma_comments = self.data.get('aroma_comments')
        obj.appearance_score = self.data.get('appearance_score')
        obj.appearance_comments = self.data.get('appearance_comments')
        obj.flavor_score = self.data.get('flavor_score')
        obj.flavor_comments = self.data.get('flavor_comments')
        obj.mouthfeel_score = self.data.get('mouthfeel_score')
        obj.mouthfeel_comments = self.data.get('mouthfeel_comments')
        obj.impression_score = self.data.get('impression_score')
        obj.impression_comments = self.data.get('impression_comments')
        return obj
