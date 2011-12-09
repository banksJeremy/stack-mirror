#!/usr/bin/env python2.7
import sqlite3
import re
import sys
import logging
import bottle

DEBUG = True
bottle.debug(DEBUG)

logger = logging.getLogger("serve_dump")
logger.setLevel(logging.INFO)
logger.addHandler(logging.NullHandler())

def serve(db, port):
    from bottle import route, view, request, run, static_file, redirect, error, abort
    
    @route("/")
    @view("views/index")
    def index():
        logger.info("Loading index.")
        questions = []
        
        with db:
            cursor = db.cursor()
            cursor.execute("SELECT Id, Title, Score, ViewCount FROM Posts Where PostTypeId = 1 ORDER BY Score DESC LIMIT 1000")
            
            for post_id, title, score, views in cursor:
                questions.append({
                    "title": title,
                    "url": "/questions/{0}/{1}".format(post_id, sluggify(title))})
        
        logger.info("Rendering index.")
        return {"questions": questions }
    
    @route("/<post_id:int>")
    @route("/q/<post_id:int>")
    @route("/questions/<post_id:int>")
    @route("/questions/<post_id:int>/")
    @route("/a/<post_id:int>")
    def to_post(post_id, referrer=None):
        pass
    
    @route("/questions/<question_id:int>/<slug>")
    @view("views/question")
    def question(question_id, slug=None):
        question = None
        answers = []
        
        with db:
            cursor = db.cursor()
            cursor.execute("""SELECT Id, Title, Body, Score, ViewCount, ParentId, OwnerUserId, OwnerDisplayName, DeletionSnapshotName
                              FROM Posts WHERE Id = ? OR ParentId = ?
                              ORDER BY Score DESC""",
                           [question_id, question_id])
            
            for post_id, title, body, score, views, parent, owner_id, owner_name, deletion in cursor:
                this = {"post_id": post_id, "title": title, "body": body, "views": views, "score": score,
                        "owner_id": owner_id, "owner_name": owner_name, "deleted": deletion}
                
                if post_id == question_id:
                    if parent and parent != post_id:
                        logger.warning("Answer ID ({0} to {1}) used in question request.".format(post_id, parent))
                        return abort(404)
                    question = this
                else:
                    answers.append(this)
        
        proper_slug = sluggify(question["title"])
        
        if slug != proper_slug:
            logger.info("Redirecting user from slug {0!r} to {1!r}.".format(slug, proper_slug))
            return redirect("/questions/{0}/{1}".format(question_id, proper_slug), 301)
        
        return {
            "question": question,
            "answers": answers,
            "canonical": "http://stackoverflow.com/q/{0}".format(question_id)
        }
    
    @route("/users/<user_id:int>/<slug>")
    @route("/u/<user_id:int>")
    @view("views/user")
    def user(user_id, slug=None):
        pass
    
    @route("/posts/<post_id:int>")
    @view("views/post")
    def post(post_id):
        pass
    
    @route("/static/<filepath:path>")
    def static(filepath):
        return static_file(filepath, root="./static")
    
    run(host="", port=port, reloader=DEBUG)

def sluggify(title):
    slug = title.lower()
    slug = slug.replace(r"\bc++\b", r"c-plus-plus")
    slug = slug.replace(r"\bc#\b", r"c-sharp")
    slug = slug.replace(r"\b\.net\b", r"dot-net"")
    slug = re.sub(r"[']", "", slug)
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", slug)
    slug = re.sub(r"\-\-+", "-", slug)
    slug = re.sub(r"(^\-|\-$|)", "", slug)
    slug = slug[:92] # maximum length
    return slug

def main(db_filename, port_s):
    logging.basicConfig(level=logging.DEBUG)
    
    db = sqlite3.connect(db_filename)
    
    logger.info("Initializing missing indexes.")
    for sql in INDEX_INITIALIZATION_SQLS:
        logger.info(sql)
        with db:
            db.execute(sql)
    
    logger.info("Initializing server.")
    serve(db, int(port_s))

INDEX_INITIALIZATION_SQLS = [
    "CREATE INDEX IF NOT EXISTS idx_User1 ON Users (DeletionSnapshotName);",
    "CREATE INDEX IF NOT EXISTS idx_User2 ON Users (DisplayName);",
    "CREATE INDEX IF NOT EXISTS idx_User3 ON Users (Reputation DESC);",
    "CREATE INDEX IF NOT EXISTS idx_Badge1 ON Badges (UserId, Name);",
    "CREATE INDEX IF NOT EXISTS idx_Badge2 ON Badges (Name);",
    "CREATE INDEX IF NOT EXISTS idx_Posts1 ON Posts (OwnerUserId, Score DESC, DeletionSnapshotName);",
    "CREATE INDEX IF NOT EXISTS idx_Posts2 ON Posts (PostTypeId, DeletionSnapshotName);",
    "CREATE INDEX IF NOT EXISTS idx_Posts3 ON Posts (DeletionSnapshotName, OwnerUserId);",
    "CREATE INDEX IF NOT EXISTS idx_Posts4 ON Posts (ParentId, Score DESC);",
    "CREATE INDEX IF NOT EXISTS idx_Posts5 ON Posts (Score DESC, ViewCount DESC);",
    "CREATE INDEX IF NOT EXISTS idx_Posts6 ON Posts (ViewCount DESC, Score DESC);",
    "CREATE INDEX IF NOT EXISTS idx_Posts9 ON Posts (CreationDate DESC);",
    "CREATE INDEX IF NOT EXISTS idx_Comments1 ON Comments (PostId, DeletionSnapshotName);",
    "CREATE INDEX IF NOT EXISTS idx_Comments2 ON Comments (UserId, DeletionSnapshotName);",
    "CREATE INDEX IF NOT EXISTS idx_Comments3 ON Comments (Score DESC, DeletionSnapshotName);",
    "CREATE INDEX IF NOT EXISTS idx_PostHistory1 ON PostHistory (PostId, RevisionGUID);",
    "CREATE INDEX IF NOT EXISTS idx_PostHistory2 ON PostHistory (UserId, PostHistoryTypeId);",
    "CREATE INDEX IF NOT EXISTS idx_PostHistory3 ON PostHistory (PostHistoryTypeId, Comment);",
    "CREATE INDEX IF NOT EXISTS idx_Votes1 ON Votes (VoteTypeID, DeletionSnapshotName, UserId);",
    "CREATE INDEX IF NOT EXISTS idx_Votes1 ON Votes (PostId, DeletionSnapshotName);",
    # "ANALYZE;",
    # "VACUUM;"
]

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
