# [so.wut.ca](http://so.wut.ca/): an unofficial Stack Overflow mirror indexing deleted questions

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


Idea: hook all links. If local, then make it an ajax request but send an out-of-band way to observe SQL queries before the page loads, then replace the loaded URL.

Eventually aggregate everything.

or at least just do the normal thing and put it in the page


`so.wut.ca` - `questions` - `users`<sub>`1114`</sub> - 

include information about indexes -- on-demand? no, when the data as a whole is requested.
make an expiring (fixed-size, rather) dictionary to hold these logs.

    class LoggingQuerier(object):
        Query = namedtuple(""LoggingQuerier.Query, "query, analysis, time")
        
        def __init__(self, db):
            self.queries = []
        
        def text_report(self):
            pass
    
    class LoggingQuerierCursor(object):
        def __init__(self, db, querier):
            self.db = db
            self.querier = querier
            self.cursor = db.cursor()
        
        __exit__
            commit or rollback
        
        def execute(self, query, *params):
            
            EXPLAIN it, then time it while you run it.
        
        def __iter__(self):
            return iter(self.cursor)

logging_querier.query("")
include a last and a first generation that it existed, and properly handle undeletion.

annotate *answers* as "deleted" when they were deleted before their post was.

I should markup the links to Stack Overflow with like a different color.

Being forced to link to the user's original profile is irritating.




Add a generic link-rewriting mechanism. Use this to rewrite Amazon links, but also to redirect any intra-SO links that we can handle ourselves.
