#!/usr/bin/env python2.7
import sqlite3
import codecs
import sys
import datetime
import re
import os
import os.path
from glob import glob
from collections import defaultdict, OrderedDict
from lxml import etree

is_numeric = re.compile(r"^[\-\+]?\d+(\.\d+)?([eE][+\-]\d+(\.\d+)?)?$").match

# used Hex Fiend to strip all "&#x00;" from the file.
# and all "&#x0A;"

def _iter_rows_of_xml(f):
    parseEvents = etree.iterparse(f, ["start"])
    _, root = next(parseEvents)
    
    for _, element in parseEvents:
        yield element

def affinities_by_name(name, cache={}):
    try:
        cache[name]
    except KeyErorr:
        if name.endswith("Date") or name == "LastAutoRename":
            cache[name] = "DATETIME"
        elif name.endswith("Id") or name.endswith("Count") or
             name.endswith("Votes") or "Rep" in name or
             name in {"Age", "Score", "Views"}:
            cache[name] = "INTEGER"
        else:
            cache[name] = "TEXT"
        
        return cache[name]

def import_xmls_to_sqlite(path, db_name):
    xmls = glob(os.path.join(path, "*.xml"))
    db_path = os.path.join(path, db_name)
    
    sys.stderr.write("db filename: " + db_path + "\n")
    db = sqlite3.connect(db_path)
    
    for xml in xmls:
        sys.stderr.write("Importing " + xml + "\n")
        
        table_name, _, _ = os.path.basename(xml).rpartition(".")
        quoted_table_name = quote_identifier(table_name)
        
        columns = OrderedDict()
        columns["Id"] = "INTEGER PRIMARY KEY"
        
        for row in _iter_rows_of_xml(xml):
            for name, value in row.items():
                if columns.setdefault(name, "NUMERIC") == "NUMERIC" and not (name.endswith("Date") or is_numeric(value)):
                    columns[name] = "TEXT"
        
        sys.stderr.write("Columns definitions generated.\n")
        
        with db:
            sql = "CREATE TABLE " + quoted_table_name + "(" + (
                ", ".join(quote_identifier(name) + " " + col_type for (name, col_type) in columns.items())
            ) + ")"
            sys.stderr.write(sql + "\n")
            db.execute(sql)
            
            sys.stderr.write("Table created.\n")
            
            for row in _iter_rows_of_xml(xml):
                keys = list(row.keys())
                values = [row.get(key) for key in keys]
                
                db.execute("INSERT INTO " + quoted_table_name + "(" + (
                    ",".join(map(quote_identifier, keys))
                ) +") VALUES (" + (
                    ",".join("?" if not key.endswith("Date") else "strftime('%s', ?)" for key in keys)
                ) + ")", values)
            
            sys.stderr.write("Data inserted.\n")
    

def main(path = ".", db_name = "dump.sqlite"):
    import_xmls_to_sqlite(path, db_name)

def create_table_from_string_maps(db, table_name, data, primary_key = "id"):
    quoted_table_name = quote_identifier(table_name)
    del table_name
    
    with db:
        db.execute("CREATE TABLE" + quoted_table_name +
                   "(" + quote_identifier(primary_key) + " INTEGER PRIMARY KEY)")
        
        
        
        for row in data:
            for key, value in row.items():
                

# all other columns are 




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
