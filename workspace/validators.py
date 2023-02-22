def validate(email):
    checker = [str(i) for i in email if (i == '.') or (i == '@')]
    if '@' in checker and '.' in checker:
        return 1
    else:
        return 0