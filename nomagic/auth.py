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


def create_user(user):
    email = user["email"]
    login = conn.get("SELECT * FROM index_login WHERE login = %s", email)
    assert not login

    user["type"] = "user"
    user["name"] = user.get("name", "")
    user["salt"] = "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    user["password"] = hashlib.sha1(user["password"] + user["salt"]).hexdigest()
    user["title"] = ""
    user["department"] = ""
    user["locatiion"] = ""
    user["mobile"] = ""
    user["tel"] = ""
    user["about"] = ""
    user["profile_img"] = ""
    user["datetime"] = datetime.datetime.now().isoformat()

    new_id = nomagic._new_key()
    rowcount = nomagic._node(new_id).execute_rowcount("INSERT INTO entities (id, body) VALUES(%s, %s)", new_id, nomagic._pack(user))
    assert rowcount

    #update indexes: email
    assert "@" in email
    rowcount = conn.execute_rowcount("INSERT INTO index_login (login, entity_id) VALUES(%s, %s)", email, new_id)
    assert rowcount

    return (new_id, user)

def update_user(user_id, data):
    #valid name
    user = nomagic._get_entity_by_id(user_id)
    user_json1 = nomagic._pack(user)
    result = {}

    if "password0" in data and "password1" in data and data["password0"] != data["password1"] and data["password1"] != "":
        #normal update password with old password0 and new password1
        if user["password"] == hashlib.sha1(data["password0"] + user.get("salt", "")).hexdigest():
            user["password"] = hashlib.sha1(data["password1"] + user.get("salt", "")).hexdigest()
            result["password_updated"] = True
        del data["password0"]
        del data["password1"]

    elif "password" in data and data["password"] != "":
        #force update password
        user["password"] = hashlib.sha1(data["password"] + user.get("salt", "")).hexdigest()
        result["password_updated"] = True
        del data["password"]

    if user:
        user.update(data)
        user_json2 = nomagic._pack(user)
        if user_json1 != user_json2:
            assert nomagic._node(user_id).execute_rowcount("UPDATE entities SET body = %s WHERE id = %s", nomagic._pack(user), nomagic._key(user_id))
    return result

def check_user(login, password):
    login_info = conn.get("SELECT entity_id FROM index_login WHERE login = %s", login)
    if login_info:
        user_id = login_info["entity_id"]
        user = nomagic._get_entity_by_id(user_id)
        if user["password"] == hashlib.sha1(password + user.get("salt", "")).hexdigest():
            return (user_id, user)
    return (None, None)

def get_user_by_login(login):
    index_login = conn.get("SELECT * FROM index_login WHERE login = %s", login)
    entity_id = index_login["entity_id"]

    return nomagic._get_entity_by_id(entity_id)

def get_user_id_by_login(login):
    index_login = conn.get("SELECT * FROM index_login WHERE login = %s", login)
    return index_login["entity_id"] if index_login else None

def email_invite(email):
    """email invite can be used for both self signup and inviting friends to join"""
    # valid email, existing in system?
    # insert into index_invite table
    token = uuid.uuid4().hex
    rowcount = conn.execute_rowcount("INSERT INTO index_invite (email, token) VALUES(%s, %s)", email, token)
    assert rowcount
    # resend? signup? invite?
    return token

