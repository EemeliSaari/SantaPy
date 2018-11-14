import optparse
import sys
import time

import config
import raffle
from sender import Sender
from database import Database
from message import Message


DB = 'db.sqlite'


def initialize_db(participants, event_name):

    with Database(DB) as db:

        if not config.check_event_exists(db, event_name):
            participants = config.setup(participants, db)

            event_name = db.add_event(event_name)

            print('\nPsst... Your event name is: {}'.format(event_name))

            db.add_participants(event_name, *participants)

            shuffled = raffle.shuffle_names(*participants)
            mapped = raffle.map_names(*shuffled)

            for secret in mapped:
                db.add_secret(event_name, *secret)

        else:
            print('\nData for event {} already exists.\n'.format(event_name))


def send_mails(template_file, event_name, wait=1):

    with Database(DB) as db:
        email_info = db.email_content(event_name)
        messages = [Message(name=m[1], subject=event_name, template=template_file) for m in email_info]
        with Sender(provider='gmail') as smtp:
            for i, msg in enumerate(messages):
                try:
                    smtp.sendmail(email_info[i][0], msg)
                except Exception:
                    print('Failed to send mail to:', email_info[i][0])
                time.sleep(wait)

    print('All the mails have been sent.')


def send_mail_by_name(name, template_file, event_name):

    with Database(DB) as db:
        email_info = db.secret_for(event_name=event_name, name=name)

    msg = Message(name=email_info[1], subject=event_name, template=template_file)

    with Sender(provider='gmail') as smtp:
        try:
            smtp.sendmail(email_info[0], msg)
        except Exception:
            print('Failed to send mail to:', email_info[0])
            return
    print('Mail sent succesfully!')


def get_events():

    with Database(DB) as db:
        event_names = db.events

    if not event_names:
        print('\nNo events available.\n')
    else:
        print('\nAvailable events:')
        list(map(lambda x: print('  - {}'.format(x[0])), event_names))


if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-t', '--template', dest='template')
    parser.add_option('-e', '--event', dest='event_name')
    parser.add_option('-p', '--participants', dest='participants')
    parser.add_option('-n', '--name', dest='participant_name')

    options, args = parser.parse_args()

    available_commands = ('new_event', 'send_mails', 'get_events', 'mail_to')

    command = sys.argv[1]
    if command == available_commands[0]:
        initialize_db(options.participants, options.event_name)
        if not options.participants:
            error = '\nProvide list of participants as json.'
            error += '\nEach element must contain a name and email.'
            print(error)
            exit()
    elif command == available_commands[1]:
        send_mails(options.template, options.event_name)
        if not options.event_name:
            print('Provide event name to send mails to.')
            exit()
    elif command == available_commands[2]:
        get_events()
    elif command == available_commands[3]:
        send_mail_by_name(options.participant_name, options.template, options.event_name)
    else:
        error = 'Provide a command for the program.'
        error += ' Available: {}'.format(', '.join(available_commands))
        print(error)
        exit()
