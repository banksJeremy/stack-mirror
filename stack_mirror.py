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
        
        with db:
            db.execute("INSERT OR IGNORE INTO Snapshots (Name) VALUES (?)", [snapshot_name])
        
        logger.info("Loading dump " + dump_root + ".")
        for table in DUMP_TABLES:
            filename = os.path.join(dump_root, table + ".xml")
            if not os.path.exists(filename):
                continue
            
            logger.info("Loading " + filename + ".")
            
            i = 0
            
            with db:
                for tag, attributes in _iter_xml(filename):
                    i += 1
                    
                    # If it doesn't have an Id, it's not a row or we don't want it.
                    if attributes.get("Id") is None:
                        continue
                    
                    keys = list(attributes.keys())
                    values = [attributes.get(key) for key in keys]
                    
                    keys.append("LastSnapshotName")
                    values.append(snapshot_name)
                    
                    if i % 10000 == 0:
                        logger.info("At " + table + "/Id " + attributes.grater("Id") + "...")
                    
                    # todo: make sure existing value doesn't have a grater snapshot_name
                    
                    sql = ("INSERT OR REPLACE INTO " + quote_identifier(table) + "(" +
                           ", ".join(quote_identifier(key) for key in keys) +
                           ") VALUES (" +
                           ", ".join("?" for key in keys) +
                           ")")
                    db.execute(sql, values)

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
    
    with open(filename) as f:
        while not done:
            while not queue:
                data = f.read(4096)
                if data:
                    parser.feed(data)
                else:
                    parser.close()
                    done = True
                    break
            
            while queue:
                yield queue.pop()
          
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
