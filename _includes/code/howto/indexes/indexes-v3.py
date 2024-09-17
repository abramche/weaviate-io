# TODO: Configure as part of the test harness

class_name = "ConfigCollection"

########################
### CLIENT CONNECTION ##
########################

import os
import weaviate

client = weaviate.Client(
    url="http://localhost:8080",
    additional_headers={"X-Cohere-Api-Key": os.getenv("COHERE_API_KEY")},
)

################################
### ENABLE HNSW - COLLECTION ###
################################

# Delete data from prior runs
if client.schema.exists(class_name):
    client.schema.delete_class(class_name)

# START EnableHNSW
class_obj = {
    "class": class_name,
    "vectorIndexType": "hnsw",
}

client.schema.create_class(class_obj)
# END EnableHNSW

class_response = client.schema.get()
schema_response = client.schema.get(class_name)

classes = []
for c in class_response["classes"]:
    classes.append(c["class"])
assert class_name in classes, "Class missing"

correct_index = False
if (schema_response["class"] == class_name) and (
    schema_response["vectorIndexType"] == "hnsw"
):
    correct_index = True
assert correct_index, "Wrong index type"


###################
### CONFIG HNSW ###
###################

# Delete data from prior runs
if client.schema.exists(class_name):
    client.schema.delete_class(class_name)

# START ConfigHNSW
class_obj = {
    "class": class_name,
    "vectorIndexType": "hnsw",
    "vectorIndexConfig": {
        "distance_metric": "cosine",
        "ef_construction": 256,  # Dynamic list size during construction
        "max_connections": 128,  # Maximum number of connections per node
        "pq": {
            "enabled": True,
        },  # Enable compression
        "ef": -1,  # Dynamic list size during search; -1 enables dynamic Ef
        "dynamic_ef_factor": 15,  # Multiplier for dynamic Ef
        "dynamic_ef_min": 200,  # Minimum threshold for dynamic Ef
        "dynamic_ef_max": 1000,  # Maximum threshold for dynamic Ef
    },
}

client.schema.create_class(class_obj)
# END ConfigHNSW

class_response = client.schema.get()
schema_response = client.schema.get(class_name)

classes = []
for c in class_response["classes"]:
    classes.append(c["class"])
assert class_name in classes, "Class missing"

correct_index = False
if (schema_response["class"] == class_name) and (
    schema_response["vectorIndexType"] == "hnsw"
):
    correct_index = True
assert correct_index, "Wrong index type"

# ##############################
# ### ENABLE HNSW - MULTIPLE ###
# ##############################

# START EnableMulti
# The Python client v3 doesn't support multiple named vectors.

# To use multiple named vectors, upgrade to the Python client v4.
# END EnableMulti

# ###################
# ### ENABLE FLAT ###
# ###################

# Delete data from prior runs
if client.schema.exists(class_name):
    client.schema.delete_class(class_name)

# START EnableFlat
class_obj = {
    "class": class_name,
    "vectorIndexType": "flat",
}

client.schema.create_class(class_obj)
# END EnableFlat

class_response = client.schema.get()
schema_response = client.schema.get(class_name)

classes = []
for c in class_response["classes"]:
    classes.append(c["class"])
assert class_name in classes, "Class missing"

correct_index = False
if (schema_response["class"] == class_name) and (
    schema_response["vectorIndexType"] == "flat"
):
    correct_index = True
assert correct_index, "Wrong index type"

######################
### CONFIGURE FLAT ###
######################

# Delete data from prior runs
if client.schema.exists(class_name):
    client.schema.delete_class(class_name)

# START ConfigFlat
class_obj = {
    "class": class_name,
    "vectorIndexType": "flat",
    "vectorIndexConfig": {
        "distance_metric": "cosine",
        "vector_cache_max_objects": 100000,
        "bq": {"enabled": True}
    },
}

client.schema.create_class(class_obj)
# END ConfigFlat

class_response = client.schema.get()
schema_response = client.schema.get(class_name)

classes = []
for c in class_response["classes"]:
    classes.append(c["class"])
assert class_name in classes, "Class missing"

correct_index = False
if (schema_response["class"] == class_name) and (
    schema_response["vectorIndexType"] == "flat"
):
    correct_index = True

assert correct_index, "Wrong index type"

######################
### ENABLE DYNAMIC ###
######################

# Delete data from prior runs
if client.schema.exists(class_name):
    client.schema.delete_class(class_name)

# START EnableDynamic
class_obj = {
    "class": class_name,
    # Additional configuration not shown
    "vectorIndexType": "dynamic",
}

client.schema.create_class(class_obj)
# END EnableDynamic

class_response = client.schema.get()
schema_response = client.schema.get(class_name)

classes = []
for c in class_response["classes"]:
    classes.append(c["class"])
assert class_name in classes, "Class missing"

correct_index = False
if (schema_response["class"] == class_name) and (
    schema_response["vectorIndexType"] == "dynamic"
):
    correct_index = True
assert correct_index, "Wrong index type"

########################
### Inverted Indexes ###
########################

# Delete data from prior runs
if client.schema.exists(class_name):
    client.schema.delete_class(class_name)

# START PropIndex
class_obj = {
    "class": class_name,
    "vectorizer": "text2vec-huggingface",
    "properties": [
        {
            "name": "title",
            "dataType": ["text"],
            "indexFilterable": True,
            "indexSearchable": True,
            "moduleConfig": {
                "text2vec-huggingface": {}
            }
        },
        {
            "name": "chunk",
            "dataType": ["int"],
            "indexRangeFilters": True,
        },
    ],
    "invertedIndexConfig": {
        "bm25": {
            "b": 0.7,
            "k1": 1.25
        },
        "indexTimestamps": True,
        "indexNullState": True,
        "indexPropertyLength": True
    }
}

client.schema.create_class(class_obj)
# END PropIndex

class_response = client.schema.get()
schema_response = client.schema.get(class_name)

classes = []
for c in class_response["classes"]:
    classes.append(c["class"])
assert class_name in classes, "Class missing"