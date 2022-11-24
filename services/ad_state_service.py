from data.database import insert_query, read_query, update_query
from data.models import AdState

def get_all_ad_states():
    data = read_query(
        ''' SELECT *
            FROM ad_states''')

    return (AdState.from_query_result(*row) for row in data)

def get_ad_state_by_id(id: int):
    data = read_query(
        ''' SELECT *
            FROM ad_states 
            WHERE id = ?''', (id,))

    return next((AdState.from_query_result(*row) for row in data), None)

def get_ad_state_by_name(status_name: str):
    data = read_query(
        ''' SELECT *
            FROM ad_states 
            WHERE name = ?''', (status_name,))

    return next((AdState.from_query_result(*row) for row in data), None)

def create_ad_state(new_state: AdState):
    generated_id = insert_query(
        'INSERT INTO ad_states(name) VALUES(?)',
        (new_state.name,))

    new_state.id = generated_id

    return new_state

def update_ad_state(new_state: AdState, old_state:AdState):
    merged = AdState(
        id= old_state.id,
        name = new_state.name or old_state.name
    )

    update_query( 
        '''UPDATE ad_states SET
           name = ?
           WHERE id = ? ''',
        (merged.name, merged.id))

    return merged

def delete_ad_state(id: int):
    update_query('DELETE FROM ad_states WHERE id = ?', (id,))
