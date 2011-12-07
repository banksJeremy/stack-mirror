# so.wut.ca: an unofficial Stack Overflow mirror indexing deleted questions

    ./so_mirror.py import data.sqlite dumps/so-2009-04...

Loads the dump into the database, using the directory's basename as the revision id.

    ./so_mirror.py update import data.sqlite stackoverflow.com 123 414 5464 657 57

Updates the specified posts' threads using the API.

    ./so_mirror.py serve data.sqlite 8080

Serve the specified database on the specified port. The index will display deleted
posts, in pages of 50, sorted by score. Non-deleted posts are available through
direct links, but they'll canonically point to the Stack Overflow post.

Question URLs should be the same as Stack Overflow's and include the URL slug.

Brainstorming for the future:
Later: pull in live data through the API. How? Who knows? Maybe whenever potentially-
stale data is requested we could send a "Refresh: 10" header and look for updates.
Include some data in the source tree: maybe every question that Joel, Jeff or I posted to, and all of the associated users/tags.
