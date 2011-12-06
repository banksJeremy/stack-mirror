#!bin/python2.7
from collections import defaultdict, OrderedDict
from glob import glob
from lxml import etree
import codecs
import datetime
import os.path
import re
import sqlite3
import sqlite3
import sys

def main(command_name, db_name, *args):
    command = {
        "update": update,
        "import": import_,
        "serve": None
    }[command_name]
    
    db = sqlite3.connect(db_name)
    db.executescript(schema)
    return command(db, *args)

API_KEY = "22lRWuqxMUOpCjzj9_4rLA"

DUMP_TABLES = [
    "badges",
    "comments",
    "posthistory",
    "posts",
    "users",
    "votes"
]

$.ajax({
    url: "http://data.stackexchange.com/stackoverflow/atom/Badges",
    headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
    },
    dataType: "json"
});

http://data.stackexchange.com/stackoverflow/atom/Users?$filter=DisplayName%20eq%20'Community'

def import_(db, *dumps):
    for dump_root in dumps:
        for table in DUMP_TABLES:
            filename = dump_root, table + ".xml"
            
            if not os.path.exists(filename):
                continue
            
            with db:
                for row in _rows_from_xml(filename):
                    # We don't import anything without an index.
                    # It's only some redundant early data and it's irritating to handle.
                    if row.get("Id") is None:
                        continue
                    
                    keys = list(row.keys())
                    values = [row.get(key) for key in keys]

def _rel(path):
    return os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), path))

with open(_rel("schema.sql")) as f:
    schema = f.read()

def _rows_from_xml(filename):
    parse_events = etree.iterparse(filename,  ["start"], parser=etree.XMLParser(recover=True))
    _, root = next(parse_events)
    
    for _, element in parse_events:
        yield element
        
        element.clear()
        del element.getparent()[0]
          
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
