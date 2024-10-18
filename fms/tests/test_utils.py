def assert_valid(client):
    assert len(client.validate()) == 0

def assert_invalid(client):
    assert len(client.validate()) != 0




