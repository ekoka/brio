from sqlalchemy import (Column, Integer, String, Unicode, DateTime, 
                        Date, Numeric, Boolean, ForeignKey)
from sqlalchemy.orm import mapper, relationship, backref

from .junctures import Juncture

class Volunteer(Juncture): 

    __tablename__ = 'volunteers'

    volunteer_id=Column(Integer, ForeignKey('junctures.juncture_id'), 
                        primary_key=True)
    firstname=Column(Unicode)
    lastname=Column(Unicode)
    phone=Column(Unicode)
    email=Column(Unicode)
    cycle=Column(Unicode) # (preschool, school, ...)
    availability=Column(Unicode) # (occasional, regular, ...)
    interests_talents=Column(Unicode)
    comments_ideas=Column(Unicode)
    optin_photos=Column(Boolean)
    optin_newsletter=Column(Boolean)

    __mapper_args__ = {'polymorphic_identity': 'volunteers'}
