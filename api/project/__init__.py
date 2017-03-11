from common.mongo import MongoLoader


def get_all_projects():
    d = MongoLoader('test', 'projects')
    return d.get_collections()


def get_project(project):
    d = MongoLoader(project, 'projects')
    return d.get_dict(project)


def create_project(project_dict, project_name):
    d = MongoLoader(project_name, 'projects')
    return d.add_dict(project_name, project_dict)


def update_project_field(project_name, field, new_value):
    d = MongoLoader(project_name, 'projects')
    return d.update_document(project_name, field, new_value)

