#!/usr/bin/env python3
import sqlite3

from .cgi_helper import print_header

conn = sqlite3.connect('web-instagram.sqlite')
c = conn.cursor()
# Create table
c.execute('''
create table users
(
	name TEXT,
	password_hash TEXT,
	salt TEXT,
	session_id TEXT,
	session_expiry TEXT,
	id INTEGER
)
;
''')

c.execute('''
create unique index users_id_uindex
	on users (id)
;
''')


# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

print_header()
print("done")