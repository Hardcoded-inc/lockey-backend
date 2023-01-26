def remove_middle_record_for(cursor, resource_field_type, id):
    query = 'DELETE FROM dbo.users_doors WHERE ' + resource_field_type + '=?;'
    cursor.execute(query, id)

