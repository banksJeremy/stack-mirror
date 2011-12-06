#!bin/python2.7
from collections import defaultdict, OrderedDict, deque
from glob import glob
from lxml import etree
import codecs
import datetime
import logging
import os.path
import re
import sqlite3
import sqlite3
import sys

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("stack_mirror")
logger.setLevel(logging.INFO)
logger.addHandler(logging.NullHandler())


def main(command_name, db_name, *args):
    command = {
        "update": None,
        "import": import_,
        "serve": None
    }[command_name]
    
    db = sqlite3.connect(db_name)
    logger.info("Connected to SQLite database " + db_name + ".")
    db.executescript(schema)
    logger.info("Initialized database as necessary.")
    return command(db, *args)

API_KEY = "22lRWuqxMUOpCjzj9_4rLA"

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
                        logger.info("At " + table + "[" + str(i) + "]" + " - " + str(competion) + " Completion - Id " + str(attributes.get("Id")) + ".")
                        db.commit()
                    
                    # If it doesn't have an Id, it's not a row or we don't want it.
                    id_ = attributes.get("Id")
                    if id_ is None:
                        continue
                    
                    cursor.execute("SELECT LastSnapshotName FROM " + quote_identifier(table) + " WHERE Id = ?", [id_])
                    previous = cursor.fetchone()
                    
                    if previous and previous[0] > snapshot_name:
                        continue
                    
                    for key, value in items:
                        if key.endwith("Date"):
                            groups = re.match(r"^(\d+)-(\d+)-(\d+)T(\d+):(\d+)(\.\d+)$", value).groups()
                            value = (datetime.datetime(int(groups[0]), int(groups[1]), int(groups[2]),
                                                       int(groups[3]), int(groups[4]), int(groups[5]),
                                                       int(float("0" + groups[6]) * 1))
                                     - datetime.datetime(1970, 1, 1)).total_seconds()
                            print value
                            items[key] = value
                     
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
                
                logger.info("Marking deleted rows.")
                sql = ("""UPDATE """ + quote_identifier(table) + """
                             SET DeletionSnapshotName = ?
                           WHERE LastSnapshotName < ?
                             AND (DeletionSnapshotName = NULL
                                   OR DeletionSnapshotName > ?)""")
                cursor.execute(sql, [snapshot_name, snapshot_name, snapshot_name])

def _rel(path):
    return os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), path))

with open(_rel("schema.sql")) as f:
    schema = f.read()

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


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
