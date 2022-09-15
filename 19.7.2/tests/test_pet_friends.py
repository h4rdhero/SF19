import pytest
from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter = ''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name = 'Bedolaga', animal_type = 'sobaka', age = '2', pet_photo = 'images/sobaka.jpeg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Bedolaga JR", "sobaka", "4", "images/sobaka1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Бедолага', animal_type='собака', age=2):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_get_api_key_for_invalid_password(email = valid_email, password = invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_all_pets_with_invalid_key(filter = ''):
    auth_key = {'key': "ytghfdbkmysqkey"}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403

def test_get_api_key_for_invalid_email(email = invalid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_add_new_pet_without_photo(name = 'OldBedolaga', animal_type = 'sobaka', age = '8'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_unsuccessful_update_self_pet_info_invalid_key(name = 'NewBedolaga', animal_type = "sobaka", age = 1):
    auth_key = {'key': "ytghfdbkmysqkey"}

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    assert status == 403