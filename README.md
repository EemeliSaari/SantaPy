# SantaPy
Small script to organize Secret Santa. Stores the secrets to the local Sqlite3 database that which the program interacts with. Program supports giving event participants in the **JSON** format.


## Requirements
The program uses the vanilla Python only. The email and smtplib libraries might not be supported in the Python versions <3.6

- Python 3.6


## Usage
Program works as a commandline tool.

```
$ python santa.py <command> [-OPTIONS]
```

Creating the participants file.
```
$ touch participants.json
...
[
  {
    "name" : "Example1",
    "email" : example1@mail.com
  },
  {
    "name" : "Example2",
    "email" : example2@mail.com
  }
]
```

Creating the event.
```
$ python santa.py new_event -p participants.json -e "My Event Name"
```

Creating the template file for the emails.
```
$ touch my_template.txt
...
Hello!

This is your Secret Santa target this year: {name}!
```

Sending the invites out.
```
$ python santa.py send_mails -t my_template.txt -e "My Event Name"
$ ...
$ Your email address: <email>
$ Your password: <password>
```
**Note:** The program uses the [smtplib](https://docs.python.org/3.6/library/smtplib.html) to login. It might require turning off the secure options with the gmail case. So using your main email is highly discouraged.

Listing the event names
```
$ python santa.py get_events
```

## Features
- Organize new events.
- List the available events.
- Send mail to the list of participants.
- Create mail using template text files.


## TODO
- Update the steps to CMD like: "Generating entries..." etc.
- Maybe read entries for persons from commandline tool
- Use a proper email provider API like Google's Gmail API.
