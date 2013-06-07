Read the code is easy!

	import uuid
	import json

Import the necessory library

	from setting import conn

Import the database connection, this connection is used for index_* tables

	from setting import ring

Import the **ring**.

**ring** is a list of connections to the databases.
	
	_NUMBER = len(ring)

**_NUMBER** is the number of database connections.

	def _pack(data): return json.dumps(data, ensure_ascii=False)

**_pack** function is used to turn data into json. We may consider to compress the data in gzip some day. however, we keep it simple now. 

	def _unpack(data): return json.loads(data)

**_unpack** is also easy to understand.

	def _key(data): return data

**_key** just be ready for future.

	def _new_key():
	    return uuid.uuid4().hex
	    #return uuid.uuid3(uuid.NAMESPACE_DNS, "yourdomain.com").hex
	    #return uuid.uuid5(uuid.NAMESPACE_DNS, "yourdomain.com").hex

**_new_key** function create a random new key with UUID.

	def _number(key): return int(key, 16) % _NUMBER

**_number** function tell the key which node of ring it should be store.

	def _get_entity_by_id(entity_id):
	    entity = ring[_number(entity_id)].get("SELECT body FROM entities WHERE id = %s", _key(entity_id))
	    return _unpack(entity["body"]) if entity else None

**_get_entity_by_id** given a entity id, return the data object(dict/list) from the certian node. 

	def _get_entities_by_ids(entity_ids):
	    entities = []
	
	    for h in range(_NUMBER):
	        ids = [str(i) for i in entity_ids if h == _number(i)]
	
	        if len(ids) > 1:
	            entities.extend([(i["id"], _unpack(i["body"])) \
	                for i in ring[h].query("SELECT * FROM entities WHERE id IN %s" % str(tuple(ids)))])
	        elif len(ids) == 1:
	            entity = _get_entity_by_id(ids[0])
	            entities.extend([(ids[0], entity)] if entity else [])
	
	    entities = dict(entities)
	    return [(i, entities[i]) for i in entity_ids]

**_get_entities_by_ids** given a list entity ids, return the data objects(dict/list) from the certian nodes.

Please take a note that the return value is a list of tuple: [(key1, data1), (key2, data2), …]

We making return value in this format for reasons:

 * the value should be returned in sequence, if this function simple return a dict, you need to sort it by **entity_ids** again.
 * the result can be easily turn to a dict by **dict(_get_entities_by_ids(entity_ids))**

Because the entities are supposed to be stored in different nodes, so this function give a help to fetch a lot of entities in one line code.

	def _update_entity_by_id(entity_id, data):
	    assert ring[_number(entity_id)].execute_rowcount("UPDATE entities SET body = %s WHERE id = %s", _pack(data), _key(entity_id))

**_update_entity_by_id** function is use to update an entity. For now, we only provide function to update one entity, because even if you have the function to do a batch, it's still be split into the same number of SQL code.

We don't provide function to delete the entity. One of reasons is that we believed data should not be delete, or you can mark them as delete, remove them out of index, but keep the data record in the database. There are some article talking about this on Internet, however it's not our topic today.