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

STACK_KEY = "22lRWuqxMUOpCjzj9_4rLA"
AMAZON_TAG = "whk5jwcq-20"

def serve(db, port):
    db.row_factory = sqlite3.Row
    
    from bottle import route, view, request, run, static_file, redirect, error, abort, template
    
    @route("/")
    def root():
        redirect("/questions")
    
    @route("/questions")
    @view("views/question-index")
    def question_index():
        with db:
            cursor = db.cursor()
            cursor.execute("""
                SELECT question.Id, question.Title, question.Score, question.ViewCount, question.DeletionSnapshotName,
                       owner.DisplayName as OwnerDisplayName
                FROM Posts question
                LEFT JOIN PostTypes type ON question.PostTypeId = type.Id
                LEFT JOIN Users owner ON question.OwnerUserId = owner.Id
                WHERE type.Name = "Question"
                ORDER BY Score DESC LIMIT 1000
            """)
            return { "rows": list(cursor) }
    
    @route("/answers")
    @view("views/answer-index")
    def answer_index():
        with db:
            cursor = db.cursor()
            cursor.execute("""
                SELECT answer.Id, answer.Score, answer.DeletionSnapshotName,
                       owner.DisplayName, owner.Id, owner.DeletionSnapshotName
                       question.Id, question.Title, question.ViewCount, question.AcceptedAnswerId
                FROM Posts answer
                JOIN Posts question ON answer.ParentId = question.Id
                LEFT JOIN PostTypes type ON answer.PostTypeId = type.Id
                LEFT JOIN Users owner ON answer.OwnerUserId = owner.Id
                WHERE type.Name = "Answer"
                ORDER BY Score DESC LIMIT 1000
            """)
            return { "rows": list(cursor) }
    
    @route("/others")
    @view("views/other-index")
    def answer_index():
        with db:
            cursor = db.cursor()
            cursor.execute("""
                SELECT post.Id, post.Title, post.Score, post.Body, post.DeletionSnapshotName,
                       parent.Id, parent.Title, parent.Score, parent.Body, parent.DeletionSnapshotName,
                       owner.DisplayName, owner.Id,
                       type.Id, type.Name
                FROM Posts post
                JOIN Posts parent ON post.ParentId = parent.Id
                LEFT JOIN PostTypes type ON post.PostTypeId = type.Id
                LEFT JOIN Users owner ON post.OwnerUserId = owner.Id
                WHERE type.Name != "Question" AND type.Name != "Answer"
                ORDER BY Score DESC LIMIT 1000
            """)
            return { "rows": list(cursor) }
    
    @route("/<post_id:int>")
    @route("/q/<post_id:int>")
    @route("/a/<post_id:int>")
    @route("/o/<post_id:int>")
    @route("/posts/<post_id:int>")
    @route("/posts/<post_id:int>")
    @route("/questions/<post_id:int>")
    @route("/questions/<post_id:int>/")
    def to_post(post_id):
        with db:
            cursor = db.cursor()
            cursor.execute("""
                SELECT t.Name, p.Id, p.Title, r.Id, r.Title
                FROM Posts p
                JOIN PostTypes t ON p.PostTypeId = t.ID
                LEFT JOIN Posts r ON p.ParentId = r.Id
                WHERE p.Id = ?""", [post_id])
            for post_type, post_id, post_title, parent_id, parent_title in cursor:
                if post_type == "Question":
                    return redirect(aurl("questions", post_id, post_title))
                elif post_type == "Answer":
                    return redirect(aurl("questions", post_id, post_title) + "#" + unicode(post_id))
                else:
                    return redirect(aurl("others", post_id))
                
                # return redirect()
            else:
                return abort(404)
    
    @route("/questions/<question_id:int>/<slug:path>")
    @view("views/question")
    def question(question_id, slug=None):
        question = None
        answers = []
        
        with db:
            cursor = db.cursor()
            cursor.execute("""SELECT Id, Title, Body, Score, ViewCount, ParentId, OwnerUserId, OwnerDisplayName, DeletionSnapshotName, Tags
                              FROM Posts WHERE Id = ? OR ParentId = ?
                              ORDER BY Score DESC""",
                           [question_id, question_id])
            
            for post_id, title, body, score, views, parent, owner_id, owner_name, deletion, tags in cursor:
                tags = re.findall("[A-Za-z0-9\-]+", tags) if tags else []
                
                body = re.sub("http://rads.stackoverflow.com/amzn/click/([^\"]+)", "http://www.amazon.com/dp/\\1?" + AMAZON_TAG, body)
                
                this = {"post_id": post_id, "title": title, "body": body, "views": views, "score": score,
                        "owner_id": owner_id, "owner_name": owner_name, "deleted": deletion, "tags": tags}
                
                if post_id == question_id:
                    if parent and parent != post_id:
                        logger.warning("Answer ID ({0} to {1}) used in question request.".format(post_id, parent))
                        return abort(404)
                    question = this
                else:
                    answers.append(this)
        
        proper_slug = sluggify(question["title"])
        
        if slug != proper_slug:
            return redirect(aurl("questions", question_id, question["title"]), 301)
        
        return {
            "question": question,
            "answers": answers,
            "canonical": "http://stackoverflow.com/q/{0}".format(question_id),
            "kspan": kspan
        }
    
    @route("/users/<user_id:int>/<slug>")
    @route("/users/<user_id:int>/")
    @route("/users/<user_id:int>")
    @route("/u/<user_id:int>")
    @view("views/user")
    def user(user_id, slug=None):
        pass
    
    @route("/others/<post_id:int>")
    @view("views/other")
    def post(post_id):
        pass
    
    @route("/static/<filepath:path>")
    def static(filepath):
        return static_file(filepath, root="./static")
    
    run(host="", port=port, reloader=DEBUG)

def kspan(n):
    if n >= 1000:
      return '<span title="{0}" data-value="{0}" class="value kilo">{1}k</span>'.format(n, n // 1000)
    else:
      return '<span title="{0}" data-value="{0}" class="value">{0}</span>'.format(n)

def aurl(*components):
    return "/" + "/".join(sluggify(unicode(component)) for component in components)

def sluggify(title):
    slug = title or ""
    slug = slug.lower()
    slug = re.sub(r"\bc\+\+\b", r"c-plus-plus", slug)
    slug = re.sub(r"\bc#(?!\w)", r"c-sharp", slug)
    slug = re.sub(r"\b\.net\b", r"dot-net", slug)
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
    "PRAGMA full_column_names=OFF;",
    # "ANALYZE;",
    # "VACUUM;"
]

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
