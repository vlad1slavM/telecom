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
    @cherrypy.tools.json_in()
    def post_equipment(self):
        equipment_json = cherrypy.request.json
        code = equipment_json.get('code')
        serial_number = equipment_json.get('serial_number')
        print(code, serial_number)
        return database.post_data(session=session, code=code, serial_number=serial_number)


if __name__ == '__main__':

    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    dispatcher.connect('get_equipment', '/api/equipment/:equipment_id', EquipmentApi().get_equipment,
                       conditions={'method': 'GET'})
    dispatcher.connect('root', '/', EquipmentApi().index)
    dispatcher.connect('get_all_equipment', '/api/equipment', EquipmentApi().get_all_equipment,
                       conditions={'method': ['GET']})
    dispatcher.connect('post_equipment', '/api/equipment', EquipmentApi().post_equipment,
                       conditions={'method': ['POST']})
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