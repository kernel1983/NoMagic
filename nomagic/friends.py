#!/usr/bin/env python
# -*- coding: utf8 -*-

import __init__ as nomagic

from setting import conn
import auth

def follow_users(user_id, friend_ids):
    user = nomagic._get_entity_by_id(user_id)
    following = user.get("following", [])
    suggested_friend_ids = user.get("suggested_friend_ids", [])
    changed = False
    for friend_id in friend_ids:
        if friend_id not in following:
            friend = nomagic._get_entity_by_id(friend_id)
            followed = friend.get("followed", [])
            if user_id not in followed:
                followed.append(user_id)
                friend["followed"] = followed
            auth.update_user(friend_id, friend)
            following.append(friend_id)
            changed = True

        if friend_id in suggested_friend_ids:
            suggested_friend_ids.remove(friend_id)
            changed = True

    if changed:
        user["following"] = following
        user["suggested_friend_ids"] = suggested_friend_ids
        auth.update_user(user_id, user)
    #followed = user.get("followed", [])


def unfollow_users(user_id, friend_ids):
    user = nomagic._get_entity_by_id(user_id)
    following = user.get("following", [])
    for friend_id in friend_ids:
        if friend_id in following:
            friend = nomagic._get_entity_by_id(friend_id)
            followed = friend.get("followed", [])
            if user_id in followed:
                followed.remove(user_id)
                friend["followed"] = followed

                auth.update_user(friend_id, friend)
            following.remove(friend_id)

    user["following"] = following
    auth.update_user(user_id, user)


def get_friends(user_ids):
    result = []
    for friend_id, friend in nomagic._get_entities_by_ids(user_ids):
        if "password" in friend:
            del friend["password"]
        if "salt" in friend:
            del friend["salt"]
        result.append(dict(friend, user_id=friend_id))

    return result
