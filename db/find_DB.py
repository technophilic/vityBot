import attendance
import dblink

from fuzzywuzzy import fuzz
import pymongo


conn = pymongo.MongoClient(dblink.host)
db = conn['chatbot-learn']
col = db.ques


def find_all(collection):
    for d in collection.find():
        yield d


def find_match(query):
    global col
    doc = None
    max = 0

    # for d in col.find():
    for d in find_all(col):
        ratio = fuzz.token_set_ratio(d['question'], query)

        if ratio > max:
            max = ratio
            doc = d

    del doc['_id']
    return doc


key = ['x_day', 'x_class', 'x_days', 'x_classes']


def get_response(query):
    """
    :return: apt response as string
    """

    matched_dbdata = find_match(query)

    # for i in key:
    #     query = matched_dbdata['question']
    #     print query
    #
    #     if i in query:
    #         # do stuff for calculation functions
    #         response = attendance.handle_query.process_query(user, query)
    #
    #         return response

    # if answer is direct
    return matched_dbdata['answer']
