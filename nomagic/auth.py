#!/usr/bin/env python
# -*- coding: utf8 -*-

import time
import datetime
import pickle
import uuid
import binascii

import zlib
#import gzip
import hashlib
import json
import random
import string

import __init__ as nomagic

from setting import conn
from setting import ring

def create_user(user):
    user["type"] = "user"
    user["name"] = user.get("name", "")
    user["password"] = ""
    user["salt"] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    user["title"] = ""
    user["department"] = ""
    user["locatiion"] = ""
    user["mobile"] = ""
    user["tel"] = ""
    user["about"] = ""
    user["profile_img"] = ""
    user["datetime"] = datetime.datetime.now().isoformat()
    new_id = nomagic._new_key()
    assert ring[nomagic._number(new_id)].execute_rowcount("INSERT INTO entities (id, body) VALUES(%s, %s)", new_id, nomagic._pack(user))

    #do we need a user_id index? currently no
    #user_id = conn.execute("INSERT INTO index_user_id (entity_id) VALUES(%s)", new_id)

    #update indexes: email
    email = user["email"]
    assert "@" in email
    assert conn.execute_rowcount("INSERT INTO index_login (login, entity_id) VALUES(%s, %s)", email, new_id)

    """
    email_host = email.split("@")[1]
    organization_id, organization = nomagic.feeds.get_organization_by_email_host(email_host)
    users = organization.get("users", [])
    users.append(new_id)
    organization["users"] = users
    _update_entity_by_id(organization_id, organization)
    """

    return (new_id, user)

def update_user(user_id, data):
    #valid name
    user = nomagic._get_entity_by_id(user_id)
    user_json1 = nomagic._pack(user)
    if user:
        user.update(data)
        user_json2 = nomagic._pack(user)
        if user_json1 != user_json2:
            assert ring[nomagic._number(user_id)].execute_rowcount("UPDATE entities SET body = %s WHERE id = %s", nomagic._pack(user), nomagic._key(user_id))

def get_user_by_email(email):
    index_login = conn.get("SELECT * FROM index_login WHERE login = %s", email)
    entity_id = index_login["entity_id"]

    return nomagic._get_entity_by_id(entity_id)

def get_user_id_by_email(email):
    index_login = conn.get("SELECT * FROM index_login WHERE login = %s", email)
    return index_login["entity_id"] if index_login else None

def email_invite(email):
    """email invite can be used for both self signup and inviting friends to join"""
    # valid email, existing in system?
    # insert into index_invite table
    token = uuid.uuid4().hex
    assert conn.execute_rowcount("INSERT INTO index_invite (email, token) VALUES(%s, %s)", email, token)
    # resend? signup? invite?
    return token
