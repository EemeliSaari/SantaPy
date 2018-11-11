import json
import os
import sqlite3


FILENAME = 'santa_participants.json'

def setup(database):
    if not os.path.exists(FILENAME):
        error = 'Setup file for Secret Santa does not exists. '
        error += 'Provide file: {}'.format(FILENAME)
        raise OSError(error)

    with open(FILENAME) as f:
        js = json.load(f)

    validate_participants(js)

    parsed_data = parse_participants(js)

    return parsed_data


def validate_participants(data):

    req = ('name', 'email')
    invalid = list(map(lambda x: not all(r in x for r in req), data))
    if any(invalid):
        filtered = [str(e) for e, x in zip(data, invalid) if x]
        error = 'Invalid entry found: {}'.format(', '.join(filtered))
        raise AssertionError(error)


def parse_participants(data):

    order = ('name', 'email')
    return tuple(tuple(x[k] for k in order) for x in data)


def check_event_exists(database, event_name):

    result = database.event_exists(event_name)[0]

    return {0:False, 1:True}[result]
