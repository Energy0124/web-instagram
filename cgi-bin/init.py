import sqlite3

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
	id INTEGER not null
)
;

create unique index users_id_uindex
	on users (id)
;



''')

# Insert a row of data
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
