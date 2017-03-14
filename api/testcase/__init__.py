# coding=utf-8
from common.mongo import get_collection, MongoLoader


def get_project_testcases(project):
    collection = get_collection(project, 'testcases')
    testcase_ids = collection.get_document_names()
    result = []
    for testcase_id in testcase_ids:
        result.append({'id': testcase_id, 'title': get_testcase(testcase_id, project)['title']})
    return result


def get_testcase(testcase_id, project):
    collection = get_collection(project, 'testcases')
    return collection.get_dict(testcase_id)


def add_testcase(testcase_dict, project):
    collection = get_collection(project, 'testcases')
    return collection.add_dict(dictionary=testcase_dict, document_name=get_last_testcase_index(project) + 1)


def update_testcase(testcase_dict, project):
    collection = get_collection(project, 'testcases')
    document_name = testcase_dict['id']
    return collection.add_dict(dictionary=testcase_dict, document_name=document_name)


def update_testcase_field(project_name, testcase, field, new_value):
    d = get_collection(project_name, 'testcases')
    return d.update_document(testcase, field, new_value)


def delete_testcase():
    return 0


def get_last_testcase_index(project):
    collection = get_collection(project, 'testcases')
    try:
        return collection.get_document_names()[-1]
    except IndexError:
        return 0
