from . import *
import sqlalchemy

class Place(Base):
  __tablename__ = 'Places'

  name            = db.Column(db.String(128), nullable =False)
  address         = db.Column(db.String(128), nullable =False)
  coast           = db.Column(db.String(128), nullable =False) # East or West
  # (Josh): @Sones just do a consistent format for state -- either California(full name) or CA (abbreviated)
  # Do whatever is easier for you (I think abbreviated might be easier since you could grab from the address)
  state           = db.Column(db.String(128), nullable =False) 
  lat             = db.Column(db.Float, nullable =False) 
  lng             = db.Column(db.Float, nullable =False) 
  reviews         = db.Column(sqlalchemy.types.ARRAY(db.String(128)))
  ratings         = db.Column(db.Float, nullable=False)
  types           = db.Column(sqlalchemy.types.ARRAY(db.String(128)))
  # (Josh): @Sones not sure if this should be an array or a single entry but it can be null in any case
  photos          = db.Column(sqlalchemy.types.ARRAY(db.String(128)), nullable=False)


  def __init__(self, **kwargs):
    self.name          = kwargs.get('name', None)
    self.address       = kwargs.get('address', None)
    self.coast         = kwargs.get('coast', None)
    self.state         = kwargs.get('state', None)
    self.lat           = kwargs.get('lat', None)
    self.lng           = kwargs.get('lng', None)
    self.reviews       = kwargs.get('reviews', None)
    self.ratings       = kwargs.get('ratings', None)
    self.types         = kwargs.get('types', None)
    self.photos        = kwargs.get('photos', None)

  def __repr__(self):
    return str(self.__dict__)


class PlaceSchema(ModelSchema):
  class Meta:
    model = Place
