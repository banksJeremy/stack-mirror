#!/usr/bin/env python2.7
from collections import defaultdict, OrderedDict, deque
from glob import glob
from lxml import etree
import codecs
import datetime
import logging
import os.path
import re
import sqlite3
import sys

logger = logging.getLogger("import_dump")
logger.setLevel(logging.INFO)
logger.addHandler(logging.NullHandler())

def main(command_name, db_name, *args):
    logging.basicConfig(level=logging.DEBUG)
    
    command = {
        "update": None,
        "import": import_
    }[command_name]
    
    db = sqlite3.connect(db_name)
    logger.info("Connected to SQLite database " + db_name + ".")
    db.executescript(INITIALIZE_IMPORT_SQL)
    logger.info("Initialized database as necessary.")
    return command(db, *args)

DUMP_TABLES = [
    "users",
    "badges",
    "posts",
    "comments",
    "posthistory",
    "votes"
]

def import_(db, *dumps):
    for dump_root in dumps:
        snapshot_name = os.path.basename(dump_root)
        
        if not snapshot_name:
            raise ValueError("specify a directory name, no trailing slash")
        
        with db:
            db.execute("INSERT OR IGNORE INTO Snapshots (Name) VALUES (?)", [snapshot_name])
        
        logger.info("Loading dump " + snapshot_name + ".")
        for table in DUMP_TABLES:
            filename = os.path.join(dump_root, table + ".xml")
            if not os.path.exists(filename):
                continue
            
            logger.info("Loading " + filename + ".")
            
            i = 0
            
            with db:
                cursor = db.cursor()
                
                for tag, attributes, competion in _iter_xml(filename):
                    if i == 1:
                        logger.debug(str(tag) + " " + str(attributes))
                    
                    i += 1
                    
                    if i % 10000 == 0:
                        logger.info("Committing {0}@{1}[{2}; {3:.1f}%]"
                                    .format(table, snapshot_name, i, competion * 100))
                        db.commit()
                    
                    # If it doesn't have an Id, it's not a row or we don't want it.
                    id_ = attributes.get("Id")
                    if id_ is None:
                        continue
                    
                    cursor.execute("SELECT LastSnapshotName FROM " + quote_identifier(table) + " WHERE Id = ?", [id_])
                    previous = cursor.fetchone()
                    
                    if previous and previous[0] > snapshot_name:
                        continue
                    
                    for key, value in attributes.items():
                        if key.endswith("Date"):
                            match = re.match(r"^(\d{4})-(\d{2})-(\d{2})(T(\d{2}):(\d{2}):(\d+)(\.\d+)?)?$", value)
                            
                            if not match:
                                logger.error("Unrecognized date format: " + repr(value))
                                break
                            
                            groups = match.groups()
                            value = (datetime.datetime(int(groups[0]), int(groups[1]), int(groups[2]),
                                                       int(groups[4] or "0"), int(groups[5] or "0"), int(groups[6] or "0"),
                                                       int(float("0" + (groups[7] or "0")) * 1))
                                     - datetime.datetime(1970, 1, 1)).total_seconds()
                            attributes[key] = value
                     
                    keys = list(attributes.keys())
                    values = [attributes.get(key) for key in keys]
                    
                    keys.append("LastSnapshotName")
                    values.append(snapshot_name)
                    
                    sql = ("INSERT OR REPLACE INTO " + quote_identifier(table) + "(" +
                           ", ".join(quote_identifier(key) for key in keys) +
                           ") VALUES (" +
                           ", ".join("?" for key in keys) +
                           ")")
                    cursor.execute(sql, values)
                
                logger.info("Table complete.")
                db.commit()
                
                logger.info("Marking deleted rows.")
                sql = ("""UPDATE """ + quote_identifier(table) + """
                             SET DeletionSnapshotName = ?
                           WHERE LastSnapshotName < ?
                             AND (DeletionSnapshotName = NULL
                                   OR DeletionSnapshotName > ?)""")
                cursor.execute(sql, [snapshot_name, snapshot_name, snapshot_name])
                
                # TODO: handle undeletion as well

class ParseStartTargetDeque(deque):
    def start(self, tag, attr):
        self.append((tag, attr))

def _iter_xml(filename):
    queue = ParseStartTargetDeque()
    parser = etree.XMLParser(recover=True, target=queue)
    done = False
    
    bytes_total = os.path.getsize(filename)
    bytes_read = 0
    
    with open(filename) as f:
        while not done:
            while not queue:
                data = f.read(4096)
                if data:
                    bytes_read += len(data)
                    parser.feed(data)
                else:
                    parser.close()
                    done = True
                    break
            
            while queue:
                yield queue.pop() + (bytes_read * 1.0 / bytes_total ,)

def quote_identifier(s, errors="strict"):
    # Quotes a SQLite identifier. Source: http://stackoverflow.com/a/6701665
    encodable = s.encode("utf-8", errors).decode("utf-8")
    
    nul_index = encodable.find("\x00")
    
    if nul_index >= 0:
        error = UnicodeEncodeError("NUL-terminated utf-8", encodable,
                                   nul_index, nul_index + 1, "NUL not allowed")
        error_handler = codecs.lookup_error(errors)
        replacement, _ = error_handler(error)
        encodable = encodable.replace("\x00", replacement)
    
    return "\"" + encodable.replace("\"", "\"\"") + "\""

INITIALIZE_IMPORT_SQL = """
PRAGMA page_size = 4096;
--PRAGMA locking_mode=EXCLUSIVE;
--PRAGMA synchronous=NORMAL;
--PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS Snapshots (
    Name                  TEXT PRIMARY KEY
);

INSERT OR IGNORE INTO Snapshots (Name) VALUES ("~preload");

CREATE TABLE IF NOT EXISTS Users (
    Id                    INTEGER PRIMARY KEY,
    LastSnapshotName      TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotName  TEXT                 REFERENCES Snapshots,
    Reputation            INTEGER NOT NULL,
    CreationDate          NUMERIC,
    DisplayName           TEXT,
    LastAccessDate        NUMERIC,
    WebsiteUrl            TEXT,
    Location              TEXT,
    AboutMe               TEXT,
    Views                 INTEGER,
    UpVotes               INTEGER,
    DownVotes             INTEGER,
    EmailHash             TEXT,
    Age                   INTEGER
);

CREATE TABLE IF NOT EXISTS Badges (
    Id                    INTEGER PRIMARY KEY,
    LastSnapshotName      TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotName  TEXT                 REFERENCES Snapshots,
    UserId                INTEGER NOT NULL     REFERENCES Users,
    Name                  TEXT    NOT NULL,
    Date                  NUMERIC
);

CREATE TABLE IF NOT EXISTS PostTypes (
    Id                    INTEGER PRIMARY KEY,
    LastSnapshotName      TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotName  TEXT                 REFERENCES Snapshots,
    Name                  TEXT    NOT NULL
);

INSERT OR IGNORE INTO PostTypes (Id, LastSnapshotName, Name) VALUES (1, "~preload", "Question");
INSERT OR IGNORE INTO PostTypes (Id, LastSnapshotName, Name) VALUES (2, "~preload", "Answer");
INSERT OR IGNORE INTO PostTypes (Id, LastSnapshotName, Name) VALUES (3, "~preload", "Tag Wiki Orphan");
INSERT OR IGNORE INTO PostTypes (Id, LastSnapshotName, Name) VALUES (4, "~preload", "Tag Wiki Excerpt");
INSERT OR IGNORE INTO PostTypes (Id, LastSnapshotName, Name) VALUES (5, "~preload", "Tag Wiki Body");
INSERT OR IGNORE INTO PostTypes (Id, LastSnapshotName, Name) VALUES (6, "~preload", "Nomination");

CREATE TABLE IF NOT EXISTS Posts (
    Id                    INTEGER PRIMARY KEY,
    PostTypeId            INTEGER NOT NULL     REFERENCES PostTypes,
    LastSnapshotName      TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotName  TEXT                 REFERENCES Snapshots,
    AcceptedAnswerId      INTEGER,
    ParentId              INTEGER              REFERENCES Posts,
    CreationDate          NUMERIC,
    Score                 INTEGER,
    ViewCount             INTEGER,
    Body                  TEXT     NOT NULL,
    OwnerUserId           INTEGER,
    OwnerDisplayName      TEXT,
    LastEditorUserId      INTEGER              REFERENCES Users,
    LastEditorDisplayName TEXT,
    LastEditDate          NUMERIC,
    LastActivityDate      NUMERIC,
    Title                 TEXT,
    Tags                  TEXT,
    AnswerCount           INTEGER,
    CommentCount          INTEGER,
    FavoriteCount         INTEGER,
    ClosedDate            NUMERIC,
    CommunityOwnedDate    NUMERIC
);

CREATE TABLE IF NOT EXISTS Comments (
    Id                    INTEGER PRIMARY KEY,
    LastSnapshotName      TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotName  TEXT                 REFERENCES Snapshots,
    PostId                INTEGER NOT NULL     REFERENCES Posts,
    Score                 INTEGER,
    Text                  TEXT    NOT NULL,
    CreationDate          NUMERIC,
    UserDisplayName       TEXT,
    UserId                INTEGER REFERENCES Users
);

CREATE TABLE IF NOT EXISTS PostHistoryTypes (
    Id                    INTEGER PRIMARY KEY,
    LastSnapshotName      TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotName  TEXT                 REFERENCES Snapshots,
    Name                  TEXT    NOT NULL
);

INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES ( 1, "~preload", "Initial Title");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES ( 2, "~preload", "Initial Body");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES ( 3, "~preload", "Initial Tags");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES ( 4, "~preload", "Edit Title");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES ( 5, "~preload", "Edit Body");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES ( 6, "~preload", "Edit Tags");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES ( 7, "~preload", "Rollback Title");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES ( 8, "~preload", "Rollback Body");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES ( 9, "~preload", "Rollback Tags");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (10, "~preload", "Post Closed");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (11, "~preload", "Post Reopened");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (12, "~preload", "Post Deleted");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (13, "~preload", "Post Undeleted");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (14, "~preload", "Post Locked");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (15, "~preload", "Post Unlocked");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (16, "~preload", "Community Owned");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (17, "~preload", "Post Migrated");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (18, "~preload", "Question Merged");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (19, "~preload", "Question Protected");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (20, "~preload", "Question Unprotected");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (21, "~preload", "Post Dissociated");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (22, "~preload", "Question Unmerged");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (23, "~preload", "(Unknown Event)");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (24, "~preload", "Suggested Edit Applied");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (25, "~preload", "Post Tweeted");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (26, "~preload", "Vote Deleted");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (27, "~preload", "Question Migrated (Silently)");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (28, "~preload", "(Unknown Event)");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (29, "~preload", "(Unknown Event)");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotName, Name) VALUES (30, "~preload", "(Unknown Event)");

CREATE TABLE IF NOT EXISTS CloseReasons (
    Id                    INTEGER PRIMARY KEY,
    LastSnapshotName      TEXT    NOT NULL     REFERENCES Snapshots,
    Name                  TEXT    NOT NULL
);

INSERT OR IGNORE INTO CloseReasons (Id, LastSnapshotName, Name) VALUES ( 1, "~preload", "Exact Duplicate");
INSERT OR IGNORE INTO CloseReasons (Id, LastSnapshotName, Name) VALUES ( 2, "~preload", "Off-Topic");
INSERT OR IGNORE INTO CloseReasons (Id, LastSnapshotName, Name) VALUES ( 3, "~preload", "Not Constructive");
INSERT OR IGNORE INTO CloseReasons (Id, LastSnapshotName, Name) VALUES ( 4, "~preload", "Not a Real Question");
INSERT OR IGNORE INTO CloseReasons (Id, LastSnapshotName, Name) VALUES ( 7, "~preload", "Too Localized");
INSERT OR IGNORE INTO CloseReasons (Id, LastSnapshotName, Name) VALUES (20, "~preload", "Noise or Pointless");

CREATE TABLE IF NOT EXISTS PostHistory (
    Id                    INTEGER PRIMARY KEY,
    LastSnapshotName      TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotName  TEXT                 REFERENCES Snapshots,
    PostHistoryTypeId     INTEGER NOT NULL     REFERENCES PostHistoryTypes,
    PostId                INTEGER NOT NULL     REFERENCES Posts,
    RevisionGUID          TEXT,
    CreationDate          NUMERIC,
    UserId                INTEGER              REFERENCES Users,
    UserDisplayName       TEXT,
    Comment               TEXT, -- if PostHistoryType == 10:
    CloseReasonId         INTEGER              REFERENCES CloseReasons,
    Text                  TEXT
);

CREATE TABLE IF NOT EXISTS VoteTypes (
    Id                    INTEGER PRIMARY KEY,
    LastSnapshotName      TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotName  TEXT                 REFERENCES Snapshots,
    Name                  TEXT NOT NULL
);

INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotName, Name) VALUES ( 1, "~preload", "AcceptedByOriginator");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotName, Name) VALUES ( 2, "~preload", "UpMod");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotName, Name) VALUES ( 3, "~preload", "DownMod");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotName, Name) VALUES ( 4, "~preload", "Offensive");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotName, Name) VALUES ( 5, "~preload", "Favorite");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotName, Name) VALUES ( 6, "~preload", "Close");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotName, Name) VALUES ( 7, "~preload", "Reopen");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotName, Name) VALUES ( 8, "~preload", "BountyStart");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotName, Name) VALUES ( 9, "~preload", "BountyClose");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotName, Name) VALUES (10, "~preload", "Deletion");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotName, Name) VALUES (11, "~preload", "Undeletion");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotName, Name) VALUES (12, "~preload", "Spam");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotName, Name) VALUES (13, "~preload", "InformModerator");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotName, Name) VALUES (14, "~preload", "(Unknown)");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotName, Name) VALUES (15, "~preload", "ModeratorReview");

CREATE TABLE IF NOT EXISTS Votes (
    Id                    INTEGER PRIMARY KEY,
    LastSnapshotName      TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotName  TEXT                 REFERENCES Snapshots,
    VoteTypeID            INTEGER              REFERENCES VoteTypes,
    PostId                INTEGER              REFERENCES Posts,
    UserId                INTEGER              REFERENCES UserId,
    CreationDate          NUMERIC,
    BountyAmount          INTEGER
);

"""

FINALIZE_IMPORT_SQL = """
PRAGMA synchronous=FULL;
PRAGMA journal_mode=DELETE;
PRAGMA locking_mode=NORMAL;
VACCUM;
"""


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
