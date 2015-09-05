from __future__ import unicode_literals
try:
    str = unicode
except:
    pass
from sqlalchemy.orm import validates
from slugify import slugify
from app import db
from app.common.models import BaseModel

STYLES = sorted((
    ('1A', 'American Light Lager - 1A'),
    ('1B', 'American Lager - 1B'),
    ('1C', 'Cream Ale - 1C'),
    ('1D', 'American Wheat - 1D'),
    ('2A', 'International Pale Lager - 2A'),
    ('2B', 'International Amber Lager - 2B'),
    ('2C', 'International Dark Lager - 2C'),
    ('3A', 'Czech Pale Lager - 3A'),
    ('3B', 'Czech Premium Pale Lager - 3B'),
    ('3C', 'Czech Amber Lager - 3C'),
    ('3D', 'Czech Dark Lager - 3D'),
    ('4A', 'Munich Helles - 4A'),
    ('4B', 'Festbier - 4B'),
    ('4C', 'Helles Bock - 4C'),
    ('5A', 'German Leichtbier - 5A'),
    ('5B', 'Kolsch - 5B'),
    ('5C', 'German Helles Exportbier - 5C'),
    ('5D', 'German Pils - 5D'),
    ('6A', 'Marzen - 6A'),
    ('6B', 'Rauchbier - 6B'),
    ('6C', 'Dunkles Bock - 6C'),
    ('7A', 'Vienna Lager - 7A'),
    ('7B', 'Altbier - 7B'),
    ('7C.1', 'Kellerbier: Pale Kellerbier - 7C.1'),
    ('7C.2', 'Kellerbier: Amber Kellerbier - 7C.2'),
    ('8A', 'Munich Dunkel - 8A'),
    ('8B', 'Schwarzbier - 8B'),
    ('9A', 'Doppelbock - 9A'),
    ('9B', 'Eisbock - 9B'),
    ('9C', 'Baltic Porter - 9C'),
    ('10A', 'Weissbier - 10A'),
    ('10B', 'Dunkles Weissbier - 10B'),
    ('10C', 'Weizenbock - 10C'),
    ('11A', 'Oridinary Bitter - 11A'),
    ('11B', 'Best Bitter - 11B'),
    ('11C', 'Strong Bitter - 11C'),
    ('12A', 'British Golden Ale - 12A'),
    ('12B', 'Australian Sparkling Ale - 12B'),
    ('12C', 'English IPA - 12C'),
    ('13A', 'Dark Mild - 13A'),
    ('13B', 'British Brown Ale - 13B'),
    ('13C', 'English Porter - 13C'),
    ('14A', 'Scottish Light - 14A'),
    ('14B', 'Scottish Heavy - 14B'),
    ('14C', 'Scottish Export - 14C'),
    ('15A', 'Irish Red Ale - 15A'),
    ('15B', 'Irish Stout - 15B'),
    ('15C', 'Irish Extra Stout - 15C'),
    ('16A', 'Sweet Stout - 16A'),
    ('16B', 'Oatmeal Sout - 16B'),
    ('16C', 'Tropical Stout - 16C'),
    ('16D', 'Foreign Extra Stout - 16D'),
    ('17A', 'British Strong Ale - 17A'),
    ('17B', 'Old Ale - 17B'),
    ('17C', 'Wee Heavy - 17C'),
    ('17D', 'English Barleywine - 17D'),
), key=lambda t: t[1])
STYLES_MAP = dict(STYLES)


class Brew(BaseModel):
    __tablename__ = "brew"
    name = db.Column(db.String(128),  nullable=False)
    slug = db.Column(db.String(255),  nullable=False, unique=True)
    brewer = db.Column(db.String(128),  nullable=False)
    email = db.Column(db.String(255), nullable=True)
    style = db.Column(db.String(10), nullable=False)
    comments = db.Column(db.Text(), nullable=True)
    brewed = db.Column(db.DateTime(), nullable=True)
    bottled = db.Column(db.DateTime(), nullable=True)
    og = db.Column(db.Float(), nullable=True)
    fg = db.Column(db.Float(), nullable=True)
    fermentables = db.Column(db.Text(), nullable=True)
    mash_schedule = db.Column(db.Text(), nullable=True)
    hops = db.Column(db.Text(), nullable=True)
    yeast = db.Column(db.String(255), nullable=True)
    reviews = db.relationship(
        'Review', backref=db.backref('person', lazy='joined'), lazy='dynamic')

    def __repr__(self):
        return self.name

    @classmethod
    def find_slug(cls, name, brewer):
        value = slugify(name)
        if not Brew.query.filter_by(slug=value).first():
            return value
        value = slugify("{} {}".format(brewer, name))
        brew = Brew.query.filter_by(slug=value).first()
        if not brew:
            return value
        index = Brew.query.filter(Brew.slug.startswith(value)).count()
        while brew:
            index += 1
            value = slugify("{} {} {}".format(brewer, name, index))
            brew = Brew.query.filter_by(slug=value).first()
        return value

    @property
    def style_name(self):
        return STYLES_MAP.get(self.style)


class Review(BaseModel):
    MAX_SCORES = {
        'aroma_score': 12,
        'appearance_score': 3,
        'flavor_score': 20,
        'mouthfeel_score': 5,
        'impression_score': 10,
        'total': 50,
    }
    __tablename__ = "review"
    brew_id = db.Column(db.Integer, db.ForeignKey('brew.id'))
    name = db.Column(db.String(128),  nullable=True)
    aroma_score = db.Column(db.Integer(), nullable=False)
    aroma_comments = db.Column(db.Text(), nullable=True)
    appearance_score = db.Column(db.Integer(), nullable=False)
    appearance_comments = db.Column(db.Text(), nullable=True)
    flavor_score = db.Column(db.Integer(), nullable=False)
    flavor_comments = db.Column(db.Text(), nullable=True)
    mouthfeel_score = db.Column(db.Integer(), nullable=False)
    mouthfeel_comments = db.Column(db.Text(), nullable=True)
    impression_score = db.Column(db.Integer(), nullable=False)
    impression_comments = db.Column(db.Text(), nullable=True)

    def __repr__(self):
        return self.name or self.email or ""

    @validates('aroma_score', 'appearance_score',
               'flavor_score', 'mouthfeel_score', 'impression_score')
    def validate_score(self, key, address):
        assert isinstance(address, int) or str(address).isdigit()
        address = int(address)
        assert 0 <= address <= self.MAX_SCORES[key]
        return address

    @property
    def total_score(self):
        return sum(getattr(self, k, 0) for k in self.MAX_SCORES.keys())
