import sys
import itertools

cols = [ 'a', 'b', 'c', 'd', 'e' ]
old_types = [ 'VARCHAR(1)', 'VARBINARY(1)', 'INT', 'CHAR(1)', 'BINARY(1)' ]
new_types = [ 'VARCHAR(2)', 'VARBINARY(2)', 'BIGINT', 'CHAR(2)', 'BINARY(2)' ]

def main():
    print "# this test generated by change_multiple.py"
    print "# this test generated multiple column changes which should all fail since we support only one at a time"
    print "--disable_warnings"
    print "DROP TABLE IF EXISTS t;"
    print "--enable_warnings"
    print "SET SESSION TOKUDB_DISABLE_SLOW_ALTER=1;"
    print "SET SESSION DEFAULT_STORAGE_ENGINE='TokuDB';"
    create_cmd = "CREATE TABLE t ("
    for i in range(len(cols)):
        create_cmd += "%s %s" % (cols[i], old_types[i])
        if i < len(cols)-1:
            create_cmd += ","
    print "%s);" % (create_cmd)
    for t in gen_comb(range(5)):
        alter_cmd = gen_alter(t)
        print "--replace_regex /MariaDB/XYZ/ /MySQL/XYZ/"
        print "--error ER_UNSUPPORTED_EXTENSION"
        print "%s;" % (alter_cmd)
    print "DROP TABLE t;"
    return 0

def gen_alter(t):
    alter = "ALTER TABLE t "
    for c in range(len(t)):
        i = t[c]
        alter += "CHANGE COLUMN %s %s %s" % (cols[i], cols[i], new_types[i])
        if c < len(t)-1:
            alter += ","
    return alter

def gen_comb(l):
    r = []
    for i in range(2,len(l)):
        r += collapse(itertools.combinations(l, i))
    return r

def collapse(i):
    r = []
    for x in i:
        r += [x]
    return r

def new_type(i):
    if i <= 0:
        return "VARCHAR(2)"
    if i <= 1:
        return "VARBINARY(2)"
    if i <= 2:
        return "BIGINT"
    if i <= 3:
        return "CHAR(2)"
    return "BINARY(2)"
sys.exit(main())
