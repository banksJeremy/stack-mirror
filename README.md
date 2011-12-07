# so.wut.ca: an unofficial Stack Overflow mirror indexing deleted questions

    ./so_mirror.py import data.sqlite dumps/so-2009-04...

Loads the dump into the database, using the directory's basename as the revision id.

    ./so_mirror.py update import data.sqlite stackoverflow.com 123 414 5464 657 57

Updates the specified posts' threads using the API.

    ./so_mirror.py serve data.sqlite 8080

Adds all of the indexes to the database.

Serve the specified database on the specified port. The index will display deleted
posts, in pages of 50, sorted by score. Non-deleted posts are available through
direct links, but they'll canonically point to the Stack Overflow post.

Question URLs should be the same as Stack Overflow's and include the URL slug.

Brainstorming for the future:
Later: pull in live data through the API. How? Who knows? Maybe whenever potentially-
stale data is requested we could send a "Refresh: 10" header and look for updates.
Include some data in the source tree: maybe every question that Joel, Jeff or I posted to, and all of the associated users/tags.

## Database 

When `./so_mirror.py import` creates a new database...

    PRAGMA page_size = 4096;

When `./so_mirror.py import` starts importing data...

    PRAGMA synchronous=NORMAL;
    PRAGMA journal_mode=WAL;
    PRAGMA locking_mode=EXCLUSIVE;

When `./so_mirror.py import` finishes importing data...

    PRAGMA synchronous=FULL;
    PRAGMA journal_mode=DELETE;
    PRAGMA locking_mode=NORMAL;
    VACCUM;

When `so_mirror` opens a database...

    INDEX ALL THE COLUMNS

