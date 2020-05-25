from Models import Engine, Base, Session

def create_database():
    print('Creating database...')
    Session.remove()
    Base.metadata.create_all(Engine)
    Session.remove()
    print('Database created successfully.')


def drop_database():
    print('Dropping database...')
    Session.remove()
    Base.metadata.drop_all(Engine, checkfirst=False)
    Session.remove()
    print('Database dropped successfully.')