from app.auth.zk_auth import create_server_signature, create_zk_instance, send_random_token, process_proof
from app import app, db
from app.models import User

from noknow import ZK

import json


zk_server, server_signature = create_server_signature()

print(server_signature)
aes_key = "320uup4ou324oiu39487304u34"

client_zk = ZK.new(curve_name="secp256k1", hash_alg="sha3_512")

signature = client_zk.create_signature(aes_key)
zk_client = create_zk_instance(signature)

param = zk_client._params

zk_client = create_zk_instance(signature)

print(zk_client._params)

del zk_client

zk_cli = ZK(param)

print(zk_cli.params)
print(zk_cli.params[2])
print(signature)
