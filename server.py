import cherrypy
from controllers import database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# create an engine object to connect to the database
engine = create_engine('mysql+mysqlconnector://user:password@localhost:3306/db')

# create a session object for database operations
Session = sessionmaker(bind=engine)
session = Session()


class EquipmentApi:

    @cherrypy.tools.json_out()
    def index(self):
        return {'message': 'Hi'}

    @cherrypy.tools.json_out()
    def get_all_equipment(self, page: int = 1, page_size: int = 10):
        return database.get_all_equipments(session=session, page=int(page), page_size=int(page_size))

    @cherrypy.tools.json_out()
    def get_equipment(self, equipment_id: int):
        """"""
        equipment = database.get_equipment_by_id(session=session, equipment_id=equipment_id)

        if equipment:
            return equipment
        else:
            raise cherrypy.HTTPError(404, f"Оборудование с id: {equipment_id} не был найден")

    @cherrypy.tools.json_out()
    def get_equipment_type(self, equipment_type_id):
        equipment_type = database.get_equipment_type_by_id(session=session, equipment_type_id=equipment_type_id)

        if equipment_type:
            return equipment_type
        else:
            raise cherrypy.HTTPError(404, f"Тип оборудования с id: {equipment_type_id} не был найден")

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def post_equipment(self):
        equipment_json = cherrypy.request.json
        code = equipment_json.get('code')
        serial_number = equipment_json.get('serial_number')
        my_response = database.post_equipment(session=session, code=code, serial_number=serial_number)
        print(my_response)
        if my_response.code == 200:
            return 'OK'
        else:
            raise cherrypy.HTTPError(my_response.code, my_response.message)

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def update_equipment(self, equipment_id):
        equipment_json = cherrypy.request.json
        code = equipment_json.get('code')
        serial_number = equipment_json.get('serial_number')
        my_response = database.update_equipment(session=session, equipment_id=equipment_id,
                                                code=code, serial_number=serial_number)
        if my_response.code == 200:
            return 'OK'
        else:
            raise cherrypy.HTTPError(my_response.code, my_response.message)

    @cherrypy.tools.json_out()
    def delete_equipment(self, equipment_id):
        my_response = database.delete_equipment(session=session, equipment_id=equipment_id)
        if my_response.code == 200:
            return 'OK'
        else:
            raise cherrypy.HTTPError(my_response.code, my_response.message)


if __name__ == '__main__':

    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    dispatcher.connect('get_equipment', '/api/equipment/:equipment_id', EquipmentApi().get_equipment,
                       conditions={'method': 'GET'})
    dispatcher.connect('get_equipment_type', '/api/equipment-type/:equipment_type_id',
                       EquipmentApi().get_equipment_type,
                       conditions={'method': 'GET'})
    dispatcher.connect('root', '/', EquipmentApi().index)
    dispatcher.connect('get_all_equipment', '/api/equipment', EquipmentApi().get_all_equipment,
                       conditions={'method': ['GET']})
    dispatcher.connect('post_equipment', '/api/equipment', EquipmentApi().post_equipment,
                       conditions={'method': ['POST']})
    dispatcher.connect('update_equipment', '/api/equipment/:equipment_id', EquipmentApi().update_equipment,
                       conditions={'method': ['PUT']})
    dispatcher.connect('delete_equipment', '/api/equipment/:equipment_id', EquipmentApi().delete_equipment,
                       conditions={'method': ['DELETE']})
    config = {
        'global': {
            'server.socket_host': '127.0.0.1',
            'server.socket_port': 8080,
            'tools.encode.on': True,
            'tools.encode.encoding': 'utf-8',
            'tools.decode.on': True,
        },
        '/': {
            'request.dispatch': dispatcher
        }
    }
    cherrypy.quickstart(None, config=config)
