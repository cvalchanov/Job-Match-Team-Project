from mariadb import IntegrityError
from data.database import insert_query, read_query, update_query
from data.models import Skill, SkillResponse, AdSkillsetResponse, Level, Skillset, SkillCategory


def get_all_skills_info(get_data_func = None):
    if get_data_func is None:
        get_data_func = read_query

    data = get_data_func(
        ''' select sc.name as category_name, s.id as skill_id, s.name as skill_name, sl.id as level_id, sl.level_name
            from skills_skill_levels as sksls
            join skill_levels as sl on sksls.skill_level_id = sl.id
            join skills as s on s.id = sksls.skill_id
            join skill_categories as sc on s.skill_category_id = sc.id
            order by sc.name''')

    return _fill_categoryskillsets(data)



def get_skillset_by_ad_id(ad_id: int, table_name, column_name, get_data_func = None):
    if get_data_func is None:
        get_data_func = read_query

    query = f''' select sc.name as category_name, s.id as skill_id, s.name as skill_name, sl.id as level_id, sl.level_name
            from skills_skill_levels as sksls
            join skill_levels as sl on sksls.skill_level_id = sl.id
            join skills as s on s.id = sksls.skill_id
            join skill_categories as sc on s.skill_category_id = sc.id
            join {table_name} as ast on sksls.skill_id = ast.skill_id and sksls.skill_level_id = ast.skill_level_id
            where ast.{column_name} = ?
            order by sc.name'''

    data = get_data_func(query, (ad_id,))
    
    return _fill_categoryskillsets(data)

def _fill_categoryskillsets(data) -> list[AdSkillsetResponse]:
    temp_skill = None
    temp_category_skillset = None
    categories_skillsets = []

    for row in range(len(data)):
        if temp_category_skillset is None:
            temp_category_skillset = AdSkillsetResponse.from_query_result(data[row][0])

            temp_skill = SkillResponse.from_query_result(data[row][1], data[row][2])
            temp_skill.level.append(Level.from_query_result(data[row][3], data[row][4]))

        elif temp_category_skillset.category_name != data[row][0]:
            temp_category_skillset.skillset.append(temp_skill)
            temp_skill = SkillResponse.from_query_result(data[row][1], data[row][2])

            categories_skillsets.append(temp_category_skillset)
            temp_category_skillset = AdSkillsetResponse.from_query_result(data[row][0])
        else:
            if temp_skill.name != data[row][1]:
                temp_category_skillset.skillset.append(temp_skill)
                temp_skill = SkillResponse.from_query_result(data[row][1], data[row][2])
            temp_skill.level.append(Level.from_query_result(data[row][3], data[row][4]))
        # To catch last row
        if row == len(data) - 1:
            temp_category_skillset.skillset.append(temp_skill)
            temp_skill.level.append(Level.from_query_result(data[row][3], data[row][4]))
            categories_skillsets.append(temp_category_skillset)

    return categories_skillsets

def add_skill_to_ad(skillset: Skillset, ad_id: int, table_name, column_name, insert_data_func = None):
    if insert_data_func is None:
        insert_data_func = insert_query

    query = f'INSERT INTO {table_name} ({column_name}, skill_id, skill_level_id) VALUES(?,?,?)'
    data = insert_data_func(query, (ad_id, skillset.skill_id, skillset.level_id))
    
    return data

def add_many_skills_to_ad(skillsets: list[Skillset], prof_ad_id: int, table_name, column_name, insert_data_func = None):
    if insert_data_func is None:
        insert_data_func = insert_query

    query = f'INSERT INTO {table_name} ({column_name}, skill_id, skill_level_id) VALUES (?,?,?)'
    parameter_list = [prof_ad_id, skillsets[0].skill_id, skillsets[0].level_id]

    for idx in range(1, len(skillsets)):
        query = f'{query}, (?,?,?)'
        parameter_list += [prof_ad_id, skillsets[idx].skill_id, skillsets[idx].level_id]

    data = insert_data_func(query, (parameter_list))
    
    return data

def create_skill(name: str, skill_category_id: int, insert_data_func = None):
    if insert_data_func is None:
        insert_data_func = insert_query

    try:
        generated_id = insert_data_func('''INSERT INTO skills(name, skill_category_id) VALUES (?,?)''',
        (name, skill_category_id))
        return Skill(id=generated_id, name=name, category_id=skill_category_id)
    except IntegrityError:
        return None

def create_skill_category(name: str, insert_data_func = None):
    if insert_data_func is None:
        insert_data_func = insert_query

    try:
        generated_id = insert_data_func('''INSERT INTO skill_categories(name) VALUES (?)''', (name,))
        return SkillCategory(id=generated_id, name=name)
    except IntegrityError:
        return None

def update_skillset(old_skillset: Skillset, new_skillset: Skillset, table_name, column_name, update_data_func = None):
    if update_data_func is None:
        update_data_func = update_query
    
    merged = Skillset(
        ad_id=old_skillset.ad_id,
        skill_id= new_skillset.skill_id or old_skillset.skill_id,
        level_id=new_skillset.level_id or old_skillset.level_id
    )
    query = f'UPDATE {table_name} SET {column_name} = ?, skill_id = ?, skill_level_id = ? WHERE {column_name} = ? AND skill_id = ? AND skill_level_id = ?'
    update_data_func(query, (new_skillset.ad_id, new_skillset.skill_id, new_skillset.level_id, old_skillset.ad_id, old_skillset.skill_id, old_skillset.level_id))
    
    return merged

def delete_from_skillsets(old_skillset: Skillset, table_name, column_name, update_data_func = None):
    if update_data_func is None:
        update_data_func = update_query
    
    query = f'DELETE from {table_name} WHERE {column_name} = ? AND skill_id = ? AND skill_level_id = ?'
    update_data_func(query, (old_skillset.ad_id, old_skillset.skill_id, old_skillset.level_id))
