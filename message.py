import plivo

AUTH_ID = 'MAZTQ5MZHLYMIXZDG2NT'
AUTH_TOKEN = 'YjhlZWU1ZjEzZmM2OTcyM2MwZjhjNzQ5ZWYxY2Fk'
SOURCE_ADDRESS = '11111111111'
DESTINATION_NUMBER = '6149065034'

def message(txt_msg='Disrupted connection!'):
    client = plivo.RestClient(auth_id=AUTH_ID, auth_token=AUTH_TOKEN)
    try:
        response = client.messages.create(
            src=SOURCE_ADDRESS,
            dst=DESTINATION_NUMBER,
            text=txt_msg,
        )
        print(response.__dict__)
    except plivo.exceptions.PlivoRestError as e:
        print(e)
