from flask import jsonify
import grovepi

PORT = 8
MOTION = 0


def get_motion_grove():
    grovepi.pinMode(PORT, "INPUT")
    MOTION = grovepi.digitalRead(PORT)
    if MOTION == 0 or MOTION == 1:
        if MOTION == 1:
            return jsonify({'motion': MOTION, 'text': 'motion detected'})
        else:
            return jsonify({'motion': MOTION, 'text': 'no motion detected'})

    else:
        return jsonify({'text': 'error'})

