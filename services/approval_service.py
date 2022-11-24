from data import database
from mariadb import IntegrityError
from data.models import AdminApprovals, ApprovalType
from services import location_service
from services import skill_service

def all(type: str = None, get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    if type:
        data = get_data_func('''SELECT * FROM approvals WHERE type = ?''', (type,))
    else:
        data = get_data_func('''SELECT * FROM approvals''')

    return [AdminApprovals.from_query_result(*row) for row in data]

def get_by_id(id: int, get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    data = get_data_func('''SELECT * FROM approvals WHERE id = ?''', (id,))

    return next((AdminApprovals.from_query_result(*row) for row in data), None)

def create(approval: AdminApprovals, insert_data_func = None):
    if insert_data_func is None:
        insert_data_func = database.insert_query

    try:
        generated_id = insert_data_func(
            '''INSERT INTO approvals(type, name, category_id) VALUES (?,?,?)''',
        (approval.type, approval.name, approval.category_id))

        return AdminApprovals(id=generated_id, type=approval.type, name=approval.name)
    except IntegrityError:
        return None


def update(old: AdminApprovals, new: AdminApprovals, update_data_func = None):
    if update_data_func is None:
        update_data_func = database.update_query

    merged = AdminApprovals(
        id = old.id,
        type = new.type,
        name = new.name,
        category_id = new.category_id)

    update_data_func('''UPDATE approvals SET type = ?, name = ?, category_id = ? WHERE id = ?''',
                        (merged.type, merged.name, merged.category_id, merged.id))

    return merged

def approve(approval: AdminApprovals):
    if approval.type == ApprovalType.SKILL_CATEGORY:
        skill_category = skill_service.create_skill_category(name=approval.name)
        delete(approval=approval)
        return skill_category
    elif approval.type == ApprovalType.SKILL:
        skill = skill_service.create_skill(name=approval.name, skill_category_id=approval.category_id)
        delete(approval=approval)
        return skill
    else:
        location = location_service.create_location(name=approval.name)
        delete(approval=approval)
        return location
       
def delete(approval: AdminApprovals, update_data_func = None):
    if update_data_func is None:
        update_data_func = database.update_query

    update_data_func('''DELETE FROM approvals WHERE id = ?''', (approval.id,))    