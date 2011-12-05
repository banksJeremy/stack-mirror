# so.wut.ca: an unofficial Stack Overflow mirror indexing deleted questions

    ./import_dump.py data.sqlite dumps/so-2009-04...

Loads the dumps into the specified database.

    ./server.py data.sqlite 8080

Serve the specified database on the specified port. The index will display deleted
posts, in pages of 50, sorted by score.

