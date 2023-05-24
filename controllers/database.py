from sqlalchemy.orm import Session

from models.equipments import Equipment, EquipmentType

from controllers.validadator import validate_serial_number
from schema import MyResponse


def get_all_equipments(session: Session, page: int = 1, page_size: int = 10) -> list[dict]:
    """
    Получить все оборудования
    :param session: сессия
    :param page: страница
    :param page_size: размер страницы
    """

    offset = (page - 1) * page_size
    equipment_query = session.query(Equipment).offset(offset).limit(page_size)

    equipments_list = []
    for equipment in equipment_query:
        user_dict = {'id': equipment.id, 'name': equipment.code_equipment_type,
                     'email': equipment.serial_number}
        equipments_list.append(user_dict)

    return equipments_list


def get_equipment_by_id(session: Session, equipment_id: int) -> dict:
    """
    Получить оборудование по ID
    :param session: сессия
    :param equipment_id: ID оборудования
    :return:
    """
    equipment = session.query(Equipment).get(equipment_id)
    equipment_dict = {'id': equipment.id, 'code': equipment.code_equipment_type,
                      'serial': equipment.serial_number}
    return equipment_dict


def get_equipment_type_by_id(session: Session, equipment_type_id: int) -> dict:
    """
    Получить тип оборудование по ID
    :param session: сессия
    :param equipment_type_id: ID типа оборудования
    :return:
    """
    equipment_type = session.query(EquipmentType).get(equipment_type_id)
    equipment_dict = {'id': equipment_type.id, 'code': equipment_type.type_name,
                      'mask': equipment_type.mask}
    return equipment_dict


def post_equipment(session: Session, code: int, serial_number: str) -> MyResponse:
    """
    Создание новой записи
    :param session: сессия
    :param code: код типа оборудования
    :param serial_number: серийный номер
    :return: Объект MyResponse(code, message)
    """
    session.begin()
    try:
        equipment_type = session.query(EquipmentType).filter(EquipmentType.id == code).one_or_none()
        if equipment_type is None:
            return MyResponse(code=404, message=f"Тип с таким id: {code} не был найден")
        mask = equipment_type.mask

        if not validate_serial_number(mask, serial_number):
            return MyResponse(code=400, message=f"Не валидный serial_number: {serial_number},"
                                                f"не соответствует маске: {mask}")
        equipment = Equipment(code_equipment_type=equipment_type.id, serial_number=serial_number)
        session.add(equipment)
        session.commit()
        return MyResponse(code=200, message="Ok")
    except Exception as e:
        session.rollback()
    finally:
        session.close()


def update_equipment(session: Session, equipment_id: int, code: int, serial_number: str) -> MyResponse:
    """
    Обновление существующей записи
    :param session: сессия
    :param equipment_id: ID существующей записи
    :param code: код типа оборудования
    :param serial_number: серийный номер
    :return: Объект MyResponse(code, message)
    """
    equipment_type = session.query(EquipmentType).filter(EquipmentType.id == code).one_or_none()
    if equipment_type is None:
        return MyResponse(code=404, message=f"Тип с таким id: {code} не был найден")

    mask = equipment_type.mask
    if not validate_serial_number(mask, serial_number):
        return MyResponse(code=400, message=f"Не валидный serial_number: {serial_number},"
                                            f"не соответствует маске: {mask}")

    else:
        equipment = session.query(Equipment).filter(Equipment.id == equipment_id).one()
        equipment.code_equipment_type = code
        equipment.serial_number = serial_number

        session.commit()
        return MyResponse(code=200, message="Ok")


def delete_equipment(session: Session, equipment_id: int) -> MyResponse:
    """
    Удалить оборудование по айди
    :param session: сессия
    :param equipment_id: айди оборудования
    """
    equipment = session.query(Equipment).filter(Equipment.id == equipment_id).one_or_none()
    if not equipment:
        return MyResponse(code=404, message=f"Тип с таким id: {equipment_id} не был найден")

    session.delete(equipment)
    session.commit()

    return MyResponse(code=200, message="Ok")
