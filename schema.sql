PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Snapshots (
    Name                  TEXT PRIMARY KEY --- precedence is determined by binary sort order.
);

INSERT OR IGNORE INTO Snapshots (Id, Name) VALUES (1000, "~preload");

CREATE TABLE IF NOT EXISTS Users (
    Id                    INTEGER PRIMARY KEY,
    LastSnapshotId        TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotId    TEXT                 REFERENCES Snapshots,
    Reputation            INTEGER,
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

INSERT OR IGNORE INTO Users (  Id, LastSnapshotId,    DisplayName, CreationDate)
                     VALUES (  -1,     "~preload"     "Community",   1217462400);
INSERT OR IGNORE INTO Users (  Id, LastSnapshotId,    DisplayName, CreationDate)
                     VALUES (   1,     "~preload",  "Jeff Atwood",   1217514151);
INSERT OR IGNORE INTO Users (  Id, LastSnapshotId,    DisplayName, CreationDate)
                     VALUES (   2,     "~preload", "Geoff Dalgas",   1217514151);
INSERT OR IGNORE INTO Users (  Id, LastSnapshotId,    DisplayName, CreationDate)
                     VALUES (   3,     "~preload", "Jarrod Dixon",   1217514151);
INSERT OR IGNORE INTO Users (  Id, LastSnapshotId,    DisplayName, CreationDate)
                     VALUES (   4,     "~preload", "Joel Spolsky",   1217514151);
INSERT OR IGNORE INTO Users (  Id, LastSnapshotId,    DisplayName, CreationDate)
                     VALUES (1114,     "~preload", "Jeremy Banks",   1218545682);

CREATE TABLE IF NOT EXISTS Badges (
    Id                    INTEGER PRIMARY KEY,
    LastSnapshotId        TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotId    TEXT                 REFERENCES Snapshots,
    UserId                INTEGER NOT NULL     REFERENCES Users,
    Name                  TEXT    NOT NULL,
    Date                  NUMERIC
);

INSERT OR IGNORE INTO Badges (  Id, LastSnapshotId,    DisplayName, CreationDate)
                      VALUES (1114,     "~preload", "Jeremy Banks",   1218545682);


CREATE TABLE IF NOT EXISTS PostTypes (
    Id                    INTEGER PRIMARY KEY,
    LastSnapshotId        TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotId    TEXT                 REFERENCES Snapshots,
    Name                  TEXT    NOT NULL
);

INSERT OR IGNORE INTO PostTypes (Id, LastSnapshotId, Name) VALUES (1, "~preload", "Question");
INSERT OR IGNORE INTO PostTypes (Id, LastSnapshotId, Name) VALUES (2, "~preload", "Answer");
INSERT OR IGNORE INTO PostTypes (Id, LastSnapshotId, Name) VALUES (3, "~preload", "Tag Wiki Orphan");
INSERT OR IGNORE INTO PostTypes (Id, LastSnapshotId, Name) VALUES (4, "~preload", "Tag Wiki Excerpt");
INSERT OR IGNORE INTO PostTypes (Id, LastSnapshotId, Name) VALUES (5, "~preload", "Tag Wiki Body");
INSERT OR IGNORE INTO PostTypes (Id, LastSnapshotId, Name) VALUES (6, "~preload", "Nomination");

CREATE TABLE IF NOT EXISTS Posts (
    Id                    INTEGER PRIMARY KEY,
    PostTypeId            INTEGER NOT NULL     REFERENCES PostTypes,
    LastSnapshotId        TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotId    TEXT                 REFERENCES Snapshots,
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
    LastSnapshotId        TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotId    TEXT                 REFERENCES Snapshots,
    PostId                INTEGER NOT NULL     REFERENCES Posts,
    Score                 INTEGER,
    Text                  TEXT    NOT NULL,
    CreationDate          NUMERIC,
    UserDisplayName       TEXT,
    UserId                INTEGER REFERENCES Users
    
);

CREATE TABLE IF NOT EXISTS PostHistoryTypes (
    Id                    INTEGER PRIMARY KEY,
    LastSnapshotId        TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotId    TEXT                 REFERENCES Snapshots,
    Name                  TEXT NOT NULL
);

INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES ( 1, "~preload", "Initial Title");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES ( 2, "~preload", "Initial Body");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES ( 3, "~preload", "Initial Tags");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES ( 4, "~preload", "Edit Title");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES ( 5, "~preload", "Edit Body");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES ( 6, "~preload", "Edit Tags");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES ( 7, "~preload", "Rollback Title");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES ( 8, "~preload", "Rollback Body");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES ( 9, "~preload", "Rollback Tags");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (10, "~preload", "Post Closed");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (11, "~preload", "Post Reopened");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (12, "~preload", "Post Deleted");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (13, "~preload", "Post Undeleted");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (14, "~preload", "Post Locked");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (15, "~preload", "Post Unlocked");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (16, "~preload", "Community Owned");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (17, "~preload", "Post Migrated");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (18, "~preload", "Question Merged");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (19, "~preload", "Question Protected");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (20, "~preload", "Question Unprotected");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (21, "~preload", "Post Dissociated");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (22, "~preload", "Question Unmerged");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (23, "~preload", "(Unknown Event)");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (24, "~preload", "Suggested Edit Applied");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (25, "~preload", "Post Tweeted");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (26, "~preload", "Vote Deleted");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (27, "~preload", "Question Migrated (Silently)");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (28, "~preload", "(Unknown Event)");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (29, "~preload", "(Unknown Event)");
INSERT OR IGNORE INTO PostHistoryTypes (Id, LastSnapshotId, Name) VALUES (30, "~preload", "(Unknown Event)");

CREATE TABLE IF NOT EXISTS CloseReasons (
    Id                    INTEGER PRIMARY KEY,
    Name                  TEXT NOT NULL
);

INSERT OR IGNORE INTO CloseReasons (Id, LastSnapshotId, Name) VALUES ( 1, "~preload", "Exact Duplicate");
INSERT OR IGNORE INTO CloseReasons (Id, LastSnapshotId, Name) VALUES ( 2, "~preload", "Off-Topic");
INSERT OR IGNORE INTO CloseReasons (Id, LastSnapshotId, Name) VALUES ( 3, "~preload", "Not Constructive");
INSERT OR IGNORE INTO CloseReasons (Id, LastSnapshotId, Name) VALUES ( 4, "~preload", "Not a Real Question");
INSERT OR IGNORE INTO CloseReasons (Id, LastSnapshotId, Name) VALUES ( 7, "~preload", "Too Localized");
INSERT OR IGNORE INTO CloseReasons (Id, LastSnapshotId, Name) VALUES (20, "~preload", "Noise or Pointless");

CREATE TABLE IF NOT EXISTS PostHistory (
    Id                    INTEGER PRIMARY KEY,
    LastSnapshotId        TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotId    TEXT                 REFERENCES Snapshots,
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

CREATE TABLE IF NOT EXISTS Tags (
    Id                    INTEGER PRIMARY KEY,
    LastSnapshotId        TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotId    TEXT                 REFERENCES Snapshots,
    Count                 INTEGER
);

--  because this has no index, 
CREATE TABLE IF NOT EXISTS PostTags (
    LastSnapshotId        TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotId    TEXT                 REFERENCES Snapshots,
    PostId                INTEGER NOT NULL     REFERENCES Posts,
    TagId                 INTEGER NOT NULL     REFERENCES Tags
);

CREATE TABLE IF NOT EXISTS TagSynonyms (
    Id                    INTEGER PRIMARY KEY,
    LastSnapshotId        TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotId    TEXT                 REFERENCES Snapshots,
    SourceTagName         TEXT,
    TargetTagName         TEXT,
    CreationDate          NUMERIC,
    OwnerUserId           INTEGER,
    AutoRenameCount       INTEGER,
    LastAutoRename        NUMERIC,
    Score                 INTEGER,
    ApprovedByUserId      INTEGER              REFERENCES Users,
    ApprovalDate          NUMERIC
);

CREATE TABLE IF NOT EXISTS VoteTypes (
    Id                    INTEGER PRIMARY KEY,
    LastSnapshotId        TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotId    TEXT                 REFERENCES Snapshots,
    Name                  TEXT NOT NULL
);

INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotId, Name) VALUES ( 1, "~preload", "AcceptedByOriginator");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotId, Name) VALUES ( 2, "~preload", "UpMod");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotId, Name) VALUES ( 3, "~preload", "DownMod");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotId, Name) VALUES ( 4, "~preload", "Offensive");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotId, Name) VALUES ( 5, "~preload", "Favorite");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotId, Name) VALUES ( 6, "~preload", "Close");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotId, Name) VALUES ( 7, "~preload", "Reopen");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotId, Name) VALUES ( 8, "~preload", "BountyStart");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotId, Name) VALUES ( 9, "~preload", "BountyClose");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotId, Name) VALUES (10, "~preload", "Deletion");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotId, Name) VALUES (11, "~preload", "Undeletion");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotId, Name) VALUES (12, "~preload", "Spam");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotId, Name) VALUES (13, "~preload", "InformModerator");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotId, Name) VALUES (14, "~preload", "(Unknown)");
INSERT OR IGNORE INTO VoteTypes (Id, LastSnapshotId, Name) VALUES (15, "~preload", "ModeratorReview");

CREATE TABLE IF NOT EXISTS Votes (
    Id                    INTEGER PRIMARY KEY,
    LastSnapshotId        TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotId    TEXT                 REFERENCES Snapshots,
    Name                  TEXT    NOT NULL    
);

CREATE TABLE IF NOT EXISTS SuggestedEdits (
    Id                    INTEGER PRIMARY KEY,
    LastSnapshotId        TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotId    TEXT                 REFERENCES Snapshots,
    CreationDate          NUMERIC,
    ApprovalDate          NUMERIC,
    RejectionDate         NUMERIC,
    OwnerUserId           INTEGER              REFERENCES Users,
    Comment               TEXT,
    Title                 TEXT,
    Tags                  TEXT,
    RevisionGUID          TEXT
);

CREATE TABLE IF NOT EXISTS SuggestedEditVotes (
    Id                    INTEGER PRIMARY KEY,
    LastSnapshotId        TEXT    NOT NULL     REFERENCES Snapshots,
    DeletionSnapshotId    TEXT                 REFERENCES Snapshots,
    UserId                INTEGER              REFERENCES Users,
    VoteTypeId            INTEGER              REFERENCES VoteTypes,
    CreationDate          NUMERIC,
    TargetUserId          INTEGER              REFERENCES Users,
    TargetRepChange       INTEGER
);
