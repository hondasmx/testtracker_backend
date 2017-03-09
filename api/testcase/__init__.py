from common.mongo import get_collection


def get_testcase(testcase_id):
    collection = get_collection('prj_test')
    return collection.get_dict(testcase_id)


def add_testcase(testcase_dict):
    collection = get_collection('prj_test')
    return collection.add_dict(dictionary=testcase_dict, document_name=testcase_dict['testcase_id'])


def delete_testcase():
    return 0

# testcase_dict = {
#     'testcase_id': 2,
#     'description': 'my second testcase',
#     'steps': [
#         'commit to hithub',
#         'go to sleep'
#     ]
# }
#
# add_testcase(testcase_dict)