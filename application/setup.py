from app import app
from Models import Engine, Base, Session, Language, Template, PostType, Capability, Role, User, Configuration
from Utils import Helper

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


def add_primary_data():

    session = Session()

    _add_primary_language(session)
    _add_primary_template(session)
    _add_primary_post_type(session)
    _add_primary_role(session)
    _add_primary_user(session)
    _add_primary_configuration(session)
    
    session.commit()


def _add_primary_language(session):

    primary_language = Language(
        name = 'Portugês',
        code = 'pt-br',
        status = 'active',
        datetime_format = '%d/%m/%Y'
    )
    session.add(primary_language)


def _add_primary_template(session):

    post_template = Template(
        name = 'Default post page template',
        description = 'Template to the default post pages',
        value = 'json-here'
    )
    session.add(post_template)

    user_template = Template(
        name = 'Default user page template',
        description = 'Template to the default user pages',
        value = 'json-here'
    )
    session.add(user_template)

    term_template = Template(
        name = 'Default term page template',
        description = 'Template to the default term pages',
        value = 'json-here'
    )
    session.add(term_template)

    static_template = Template(
        name = 'Default static page template',
        description = 'Template to the default static pages',
        value = 'json-here'
    )
    session.add(static_template)

    nested_template = Template(
        name = 'Default nested page template',
        description = 'Template to the default nested pages',
        value = 'json-here'
    )
    session.add(nested_template)


def _add_primary_post_type(session):

    session.flush()

    post_type_post = PostType(
        name = 'Post Type to default posts',
        type = 'post-page',
        template_id = 1
    )
    session.add(post_type_post)

    post_type_user = PostType(
        name = 'Post Type to default user pages',
        type = 'user-profile',
        template_id = 2
    )
    session.add(post_type_user)

    post_type_term = PostType(
        name = 'Post Type to default term pages',
        type = 'term-page',
        template_id = 3
    )
    session.add(post_type_term)

    post_type_static = PostType(
        name = 'Post Type to default static pages',
        type = 'static-page',
        template_id = 4
    )
    session.add(post_type_static)

    post_type_nested = PostType(
        name = 'Post Type to default nested pages',
        type = 'nested-page',
        template_id = 5
    )
    session.add(post_type_nested)


def _add_primary_role(session):

    session.flush()

    primary_capability = Capability(
        description = 'Primary capability',
        type = 'type-here',
        target_id = 1,
        can_write = True,
        can_read = True,
        can_delete  = True
    )
    admin_role = Role(
        name = 'Administrator',
        description = 'Full access aplication',
        can_access_admin = True
    )
    admin_role.capabilities.append(primary_capability)

    session.add(admin_role)


def _add_primary_user(session):

    session.flush()

    primary_user = User(
        login = 'admin',
        password = 'admin123',
        nickname = 'admin',
        first_name = 'Admin',
        last_name = 'Admin',
        email = 'admin@email.com',
        registered = Helper().get_current_datetime(),
        status = 'active',
        role_id = 1
    )
    session.add(primary_user)


def _add_primary_configuration(session):

    session.flush()

    primary_config = Configuration(
        title = 'CMSYS - Content Management System.',
        description = 'An API FLASK to content management system.',
        has_comments = False,
        email = 'site@email.com',
        language_id = 1
    )
    session.add(primary_config)