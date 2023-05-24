from sqlalchemy import Engine
from sqlalchemy.orm import Session

from db import Equipment, EquipmentType
from sqlalchemy.orm.exc import NoResultFound

from controllers.validadator import validate_serial_number


def get_all_equipments(session: Session, page: int = 1, page_size: int = 10):
    offset = (page - 1) * page_size
    equipment_query = session.query(Equipment).offset(offset).limit(page_size)

    equipments_list = []
    for equipment in equipment_query:
        user_dict = {'id': equipment.id, 'name': equipment.code_equipment_type,
                     'email': equipment.serial_number}
        equipments_list.append(user_dict)

    return equipments_list


def get_equipment_by_id(session: Session, equipment_id: int):
    """"""
    try:
        equipment = session.query(Equipment).get(equipment_id)
        equipment_dict = {'id': equipment.id, 'code': equipment.code_equipment_type,
                          'mask': equipment.serial_number}
        return equipment_dict
    except NoResultFound:
        raise Exception(f"Оборудование с id: {equipment_id} не был найден")


def post_data(session: Session, code: int, serial_number: str):
    session.begin()
    try:
        equipment_type = session.query(EquipmentType).filter(EquipmentType.id == code).one_or_none()
        if equipment_type is None:
            session.close()
            raise Exception(f"Тип с таким id: {code} не был найден")
        mask = equipment_type.mask

        if not validate_serial_number(mask, serial_number):
            session.close()
            raise Exception(f"Invalid Serial Number: {serial_number}, does not match mask: {mask}")
        equipment = Equipment(code_equipment_type=equipment_type.id, serial_number=serial_number)
        session.add(equipment)
        session.commit()
        session.close()
        equipment_dict = {'id': equipment.id,
                          'code_equipment_type': equipment.code_equipment_type,
                          'serial_number': equipment.serial_number}
        return equipment_dict
    except Exception as e:
        session.rollback()
