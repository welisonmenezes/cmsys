from flask import current_app, Blueprint, render_template, request, url_for, redirect, flash, session, jsonify
from app import app

from Database import Session, Customers

DashboardController = Blueprint('DashboardController', __name__, url_prefix='/admin', template_folder='Views', static_folder='static')

@DashboardController.route('/')
def index():

    # add
    '''
    session = Session()
    c1 = Customers(name = 'Giovana Menezes', address = 'Universitário, Coral.', email = 'giovana@gmail.com')
    session.add(c1)
    session.commit()
    session.close()
    '''


    # consultar
    '''
    session = Session()
    result = session.query(Customers).all()
    for row in result:
        print ("Name: ",row.name, "Address:",row.address, "Email:",row.email)
    '''


    # editar
    '''
    session = Session()
    x = session.query(Customers).get(2)
    print ("Name: ", x.name, "Address:", x.address, "Email:", x.email)
    x.name = 'Iracema Siqueira'
    x.address = 'Quinta Lebrão, Teresópolis'
    x.email = 'iracema@hotmail.com'
    session.commit()
    '''


    # filtro
    '''
    session = Session()
    result = session.query(Customers).filter(Customers.name.like('Gi%'))
    #result = session.query(Customers).filter(Customers.id>2)
    #print(result)
    for row in result:
        print ("Name: ",row.name, "Address:",row.address, "Email:",row.email)
    '''


    # textual sql
    '''
    session = Session()
    #result = session.query(Customers).filter(text('id = :value')).params(value = 1)
    result = session.query(Customers).from_statement(text("SELECT * FROM customers")).all()
    #result = session.query(Customers).filter(text("id<3"))
    #print(result)
    for row in result:
        print ("Name: ",row.name, "Address:",row.address, "Email:",row.email)
    '''


    # many to many (from parent)
    '''
    session = Session()
    result = session.query(Parent).all()
    for row in result:
        print ('Id: ', row.id, 'Name: ', row.name)
        if row.children:
            for rowc in row.children:
                print('     - Id: ', rowc.id, 'Value: ', rowc.value)
    '''


    # many to many (from child)
    '''
    session = Session()
    result = session.query(Child).all()
    for row in result:
        print ('Id: ', row.id, 'Name: ', row.name)
        if row.children:
            for rowc in row.children:
                print('     - Id: ', rowc.id, 'Name: ', rowc.child.name, 'Value: ', rowc.value)
    '''


    # many to many (from association)
    '''
    session = Session()
    result = session.query(Association).all()
    for row in result:
        print ('Id: ', row.id, 'Value: ', row.value, 'Child: ', row.child.name, 'Parent:', row.parent.name)
    '''



    # manu to many (create)
    '''
    session = Session()

    p = Parent(name="Pai Um")
    a = Association(value="Assoc Um")
    a.child = Child(name="Child Um")

    a2 = Association(value="Assoc Dois")
    a2.child = Child(name="Child Dois")

    p.children.append(a)
    p.children.append(a2)

    session.add(p)
    session.commit()
    session.close()
    '''


    # many to many (add child)
    '''
    session = Session()
    pai = session.query(Parent).first()
    filho = session.query(Child).get(5)

    newassoc = Association(value="Nova associação")
    newassoc.child = filho

    pai.children.append(newassoc)
    session.commit()
    session.close()
    '''


    # many to many (delete association)
    '''
    session = Session()
    result = session.query(Association).filter(Association.child == None)
    for row in result:
        session.delete(row)
    session.commit()
    session.close()
    '''

    return render_template('index.html')