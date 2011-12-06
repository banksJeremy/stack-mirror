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

API_KEY = "22lRWuqxMUOpCjzj9_4rLA"

def _rel(path):
    return os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), path))

with open(_rel("schema.sql")) as f:
    schema = f.read()

tables = [
    "users",
    "badges",
    "posttypes",
    "posts",
    "comments",
    "posthistorytypes",
    "posthistory",
    "tags",
    "posttags",
    "votetypes"
]

def import_(db, *dumps):
    for dump_root in dumps:
        xml = os.path.join(dump_root, "*.xml")
        

def main(command_name, db_name, *args):
    command = {
        "update": update,
        "import": import_,
        "serve": None
    }[command_name]
    
    db = sqlite3.connect(db_name)
    db.executescript(schema)
    return command(db, *args)

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))

