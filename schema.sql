CREATE TABLE IF NOT EXISTS Dumps (
    Id                    INTEGER PRIMARY KEY,
    Name                  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Users (
    Id                    INTEGER PRIMARY KEY,
    LastDumpId            INTEGER NOT NULL     REFERENCES Dumps,
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

CREATE TABLE IF NOT EXISTS Badges (
    Id                    INTEGER PRIMARY KEY,
    UserId                INTEGER NOT NULL     REFERENCES Users,
    LastDumpId            INTEGER NOT NULL     REFERENCES Dumps,
    Name                  TEXT    NOT NULL,
    Date                  NUMERIC
);

CREATE TABLE IF NOT EXISTS PostTypes (
    Id                    INTEGER PRIMARY KEY,
    LastDumpId            INTEGER NOT NULL     REFERENCES Dumps,
    Name                  TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS Posts (
    Id                    INTEGER PRIMARY KEY,
    PostTypeId            INTEGER NOT NULL     REFERENCES PostTypes,
    LastDumpId            INTEGER NOT NULL     REFERENCES Dumps,
    AcceptedAnswerId      INTEGER,
    ParentId              INTEGER              REFERENCES Posts
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
    LastDumpId            INTEGER NOT NULL     REFERENCES Dumps,
    PostId                INTEGER NOT NULL     REFERENCES Posts,
    Score                 INTEGER,
    Text                  TEXT    NOT NULL,
    CreationDate          NUMERIC,
    UserDisplayName       TEXT,
    UserId                INTEGER REFERENCES Users;
    
);

CREATE TABLE IF NOT EXISTS PostHistoryTypes (
    Id                    INTEGER PRIMARY KEY,
    LastDumpId            INTEGER NOT NULL     REFERENCES Dumps,
    Name                  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS PostHistory (
    Id                    INTEGER PRIMARY KEY,
    PostHistoryTypeId     INTEGER NOT NULL     REFERENCES PostHistoryTypes,
    LastDumpId            INTEGER NOT NULL     REFERENCES Dumps,
    PostId                INTEGER NOT NULL     REFERENCES Posts,
    RevisionGUID          TEXT,
    CreationDate          NUMERIC,
    UserId                INTEGER              REFERENCES Users,
    UserDisplayName       TEXT,
    Comment               TEXT,
    Text                  TEXT
);

CREATE TABLE IF NOT EXISTS Tags (
    Id                    INTEGER PRIMARY KEY,
    LastDumpId            INTEGER NOT NULL     REFERENCES Dumps,
    Count                 INTEGER
);

CREATE TABLE IF NOT EXISTS PostTags (
    LastDumpId            INTEGER NOT NULL     REFERENCES Dumps,
    PostId                INTEGER NOT NULL     REFERENCES Posts,
    TagId                 INTEGER NOT NULL     REFERENCES Tags
);

CREATE TABLE IF NOT EXISTS TagSynonyms (
    Id                    INTEGER PRIMARY KEY,
    LastDumpId            INTEGER NOT NULL     REFERENCES Dumps,
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
    LastDumpId            INTEGER NOT NULL     REFERENCES Dumps,
    Name                  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Votes (
    Id                    INTEGER PRIMARY KEY,
    LastDumpId            INTEGER NOT NULL     REFERENCES Dumps,
    Name                  TEXT    NOT NULL    
);

CREATE TABLE IF NOT EXISTS SuggestedEdits (
    Id                    INTEGER PRIMARY KEY,
    LastDumpId            INTEGER NOT NULL     REFERENCES Dumps,
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
    LastDumpId            INTEGER NOT NULL     REFERENCES Dumps,
    UserId                INTEGER              REFERENCES Users,
    VoteTypeId            INTEGER              REFERENCES VoteTypes,
    CreationDate          NUMERIC,
    TargetUserId          INTEGER              REFERENCES Users,
    TargetRepChange       INTEGER
);
