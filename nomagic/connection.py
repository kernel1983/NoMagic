#!/usr/bin/env python
# -*- coding: utf8 -*-

import time
import datetime
import pickle
import uuid
import binascii

import zlib
import hashlib
import json
import random
import string

import __init__ as nomagic

from setting import conn


def connect_index_and_entity(table_index, index_name, index_connection_name, entity_id, entity_connection_name):
    index = conn.get("SELECT * FROM %s WHERE name = %s" % (table_index, "%s"), index_name)
    index_data = nomagic._unpack(index["data"] or "{}")
    index_connection = set(index_data.get(index_connection_name, []))
    if entity_id not in index_connection:
        index_connection.add(entity_id)
        index_data[index_connection_name] = list(index_connection)
        index_data_updated = nomagic._pack(index_data)
        conn.execute("UPDATE %s SET data = %s WHERE name = %s" % (table_index, "%s", "%s"), index_data_updated, index_name)

    entity = nomagic._get_entity_by_id(entity_id)
    entity_connection = set(entity.get(entity_connection_name, []))
    if index_name not in entity_connection:
        entity_connection.add(index_name)
        entity[entity_connection_name] = list(entity_connection)
        nomagic._update_entity_by_id(entity_id, entity)


def disconnect_index_and_entity(table_index, index_name, index_connection_name, entity_id, entity_connection_name):
    index = conn.get("SELECT * FROM %s WHERE name = %s" % (table_index, "%s"), index_name)
    index_data = nomagic._unpack(index["data"] or "{}")
    index_connection = set(index_data.get(index_connection_name, []))
    if entity_id in index_connection:
        index_connection.remove(entity_id)
        index_data[index_connection_name] = list(index_connection)
        index_data_updated = nomagic._pack(index_data)
        conn.execute("UPDATE %s SET data = %s WHERE name = %s" % (table_index, "%s", "%s"), index_data_updated, index_name)

    entity = nomagic._get_entity_by_id(entity_id)
    entity_connection = set(entity.get(entity_connection_name, []))
    if index_name in entity_connection:
        entity_connection.remove(index_name)
        entity[entity_connection_name] = list(entity_connection)
        nomagic._update_entity_by_id(entity_id, entity)


def connect_entities(entity_id1, entity_connection_name1, entity_id2, entity_connection_name2):
    entity1, entity2 = nomagic._get_entities_by_ids([entity_id1, entity_id2])
    entity_data1, entity_data2 = entity1[1], entity2[1]

    entity_connection = set(entity_data1.get(entity_connection_name1, []))
    if entity_id2 not in entity_connection:
        entity_connection.add(entity_id2)
        entity_data1[entity_connection_name1] = list(entity_connection)
        nomagic._update_entity_by_id(entity_id1, entity_data1)

    entity_connection = set(entity_data2.get(entity_connection_name2, []))
    if entity_id1 not in entity_connection:
        entity_connection.add(entity_id1)
        entity_data2[entity_connection_name2] = list(entity_connection)
        nomagic._update_entity_by_id(entity_id2, entity_data2)


def disconnect_entities(entity_id1, entity_connection_name1, entity_id2, entity_connection_name2):
    entity1, entity2 = nomagic._get_entities_by_ids([entity_id1, entity_id2])
    entity_data1, entity_data2 = entity1[1], entity2[1]

    entity_connection = set(entity_data1.get(entity_connection_name1, []))
    if entity_id2 in entity_connection:
        entity_connection.remove(entity_id2)
        entity_data1[entity_connection_name1] = list(entity_connection)
        nomagic._update_entity_by_id(entity_id1, entity_data1)

    entity_connection = set(entity_data2.get(entity_connection_name2, []))
    if entity_id1 in entity_connection:
        entity_connection.remove(entity_id1)
        entity_data2[entity_connection_name2] = list(entity_connection)
        nomagic._update_entity_by_id(entity_id2, entity_data2)

if __name__ == '__main__':
    pass
