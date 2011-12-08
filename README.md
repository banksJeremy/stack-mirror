# so.wut.ca: an unofficial Stack Overflow mirror indexing deleted questions

    ./import_dump.py data.sqlite dumps/so-2009-*

Loads the dump into the database, using the directory's basename as the revision id (relevant!).

    ./serve_dump.py date.sqlite 8080

Indexes the database, then serves it! The home will display deleted
posts, in pages of 50, sorted by score. Non-deleted posts are available through
direct links, but they'll canonically point to the Stack Overflow post.



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

