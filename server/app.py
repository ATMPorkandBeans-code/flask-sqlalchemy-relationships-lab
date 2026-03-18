#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate
from datetime import datetime

from models import db, Event, Session, Speaker, Bio, SessionSpeakers

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/events')
def get_events():
    all_events = []
    events = Event.query.all()

    if events:
        for event in events:
            event_dict = {
                'id': event.id,
                'location': event.location,
                'name': event.name
            }
            all_events.append(event_dict)
        return jsonify(all_events)
    else:
        body = {'message': 'Events not found.'}
        status = 404
    
    return jsonify(body, status)


@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    sessions = Session.query.filter_by(event_id=id).all()
    all_sessions = []

    if not sessions:
        return jsonify({"error": "Event not found"}), 404

    for session in sessions:
        formatted_time = session.start_time.isoformat()
        session_dict = {
                'id': session.id,
                'title': session.title,
                'start_time': formatted_time
            }
        all_sessions.append(session_dict)
    return jsonify(all_sessions)


@app.route('/speakers')
def get_speakers():
    all_speakers = []
    speakers = Speaker.query.all()
    
    if not speakers:
        return jsonify({"error": "Event not found"}), 404
    
    for speaker in speakers:
        speaker_dict = {
            'id': speaker.id,
            'name': speaker.name
        }
        all_speakers.append(speaker_dict)
        return jsonify(all_speakers)
    
    # return jsonify(body, status)


@app.route('/speakers/<int:id>')
def get_speaker(id):
    speaker = Speaker.query.filter(Speaker.id == id).first()
    bio = Bio.query.filter_by(speaker_id=id).first()

    if not speaker:
        return jsonify({"error": "Speaker not found"}), 404

    if bio:
        bio_text = bio.bio_text
    else:
        bio_text = "No bio available" 
    body = {
            'id': speaker.id,
            'name': speaker.name,
            'bio_text': bio_text
        }
    return (body)


@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    session = Session.query.filter_by(id=id).first()
    all_speakers = []

    if not session:
        return jsonify({"error": "Session not found"}), 404
 
    for speaker in session.speakers:
        bio = Bio.query.filter(Bio.id == speaker.id).first()
        if bio:
                bio_text = bio.bio_text
        else:
                bio_text = "No bio available"

        all_speakers.append({
                "id": speaker.id,
                "name": speaker.name,
                "bio_text": bio_text
            })
        return jsonify(all_speakers)


if __name__ == '__main__':
    app.run(port=5555, debug=True)