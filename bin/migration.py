import sys
import pickle
import uuid
import binascii
import json
import zlib

sys.path.append("..")

from setting import settings
from setting import conn
from setting import ring

import nomagic
from nomagic import _RING

_NUMBER = len(ring)

def _number(key): return int(key, 16) % _NUMBER

def _node(key): return ring[_RING.get_node(key)]


for r in ring:
    offset = 0
    ids_to_delete = []
    while True:
        users = r.query("SELECT * FROM entities ORDER BY auto_increment LIMIT %s, 100", offset)

        if len(users) == 0:
            break

        for user in users:
            user_id = str(user["id"])
            print user["id"], _number(user_id), nomagic._RING.get_node(user_id)
            if r is not _node(user_id):
                _node(user_id).execute_rowcount("INSERT INTO entities (id, body) VALUES (%s, %s)", user["id"], user["body"])
                ids_to_delete.append(user_id)

        offset += 100

    for id_to_delete in ids_to_delete:
        print r.execute_rowcount("DELETE FROM entities WHERE id = %s", id_to_delete)
