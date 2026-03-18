from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class SessionSpeakers(db.Model):
    __tablename__ = 'session_speakers'

    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
    speaker_id = db.Column(db.Integer, db.ForeignKey('speakers.id'))

    session = db.relationship('Session', back_populates='session_speakers')
    speaker = db.relationship('Speaker', back_populates='session_speakers')

    def __repr__(self):
        return f'''<Session ID is {self.id}, Session is {self.session.title}, Start Time is 
        {self.session.start_time}, Speaker is {self.speaker.name}>'''


# TODO: set up relationships for all models
class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    session_id = db.Column(db.Integer)

    sessions = db.relationship('Session', back_populates='event')

    def __repr__(self):
        return f'<Event {self.id}, {self.name}, {self.location}>'

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    
    session_speakers = db.relationship(
        'SessionSpeakers', back_populates='session', cascade='all, delete-orphan')
    
    speakers = association_proxy("session_speakers", "speaker",
    creator=lambda speaker: SessionSpeakers(speaker=speaker))
    
    event = db.relationship('Event', back_populates="sessions")


    def __repr__(self):
        return f'<Session {self.id}, {self.title}, {self.start_time}>'


class Speaker(db.Model):
    __tablename__ = 'speakers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    bio = db.relationship('Bio', uselist=False, back_populates='speaker', cascade='all, delete-orphan')

    session_speakers = db.relationship(
        'SessionSpeakers', back_populates='speaker',cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Speaker {self.id}, {self.name}>'

class Bio(db.Model):
    __tablename__ = 'bios'

    id = db.Column(db.Integer, primary_key=True)
    bio_text = db.Column(db.Text, nullable=False)
    speaker_id = db.Column(db.Integer, db.ForeignKey('speakers.id'))

    speaker = db.relationship('Speaker', back_populates='bio')

    def __repr__(self):
        return f'<Bio {id}, {self.bio_text}>'
