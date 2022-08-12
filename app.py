from flask import Flask, request, jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('office', user='denny', password='123',
                        host='localhost', port=5432)

class BaseModel(Model):
    class Meta:
        database = db

class Staff(BaseModel):
    first_name = CharField()
    last_name = CharField()
    age = IntegerField()

db.connect()
db.drop_tables([Staff])
db.create_tables([Staff])

Staff(first_name='Michael', last_name='Scott', age=57).save()
Staff(first_name='Dwight', last_name='Schrute', age=52).save()
Staff(first_name='Jim', last_name='Halpert', age=43).save()
Staff(first_name='Pam', last_name='Beesly', age=43).save()
Staff(first_name='Stanley', last_name='Hudson', age=71).save()
Staff(first_name='Creed', last_name='Bratton', age=96).save()

app = Flask(__name__)

@app.route('/person', methods=['GET', 'POST'])
@app.route('/person/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Staff.get(Staff.id==id)))
        else:
            staff_list = []
            for staff in Staff.select():
                staff_list.append(model_to_dict(staff))
            return jsonify(staff_list)

    if request.method == 'PUT':
        try:
            Staff.get(Staff.id == id)
            body = request.get_json()
            Staff.update(body).where(Staff.id == id).execute()
            return jsonify({f'ID: {id}': 'Success'})
        except:
            return jsonify({f'ID: {id}': 'Failed to update'})

    if request.method == 'POST':
        new_staff = dict_to_model(Staff, request.get_json())
        new_staff.save()
        return jsonify({'success': True})

    if request.method == 'DELETE':
        if id:
            Staff.delete().where(Staff.id == id).execute()
            return jsonify({f'ID: {id}': 'Deleted'})
        else:
            return jsonify({f'ID: {id}': 'Does not exist'})

app.run(port=5000, debug=True)