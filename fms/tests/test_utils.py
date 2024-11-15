def assert_valid(client):
    assert len(client.validate()) == 0

def assert_invalid(client):
    assert len(client.validate()) != 0

def sensor_in_list(name, sensor_list):
    for sensor in sensor_list:
        if sensor[0] == name:
            return True
    return False

def remove_sensor_in_list(name, sensor_list):
    sensor_list = [sensor for sensors in sensor_in_list if sensor[0] != name]


