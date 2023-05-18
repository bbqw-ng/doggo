def upload_image(file, name, column, storage, mycursor, db):
    storage.child(name + "/" + column).put(file)
    url = storage.child(name + "/" + column).get_url(None)
    query = f"UPDATE LoginInfo SET {column} = %s WHERE username = %s"
    values = (url, name)
    mycursor.execute(query, values)
    db.commit()
    print(mycursor.rowcount, "record(s) affected")