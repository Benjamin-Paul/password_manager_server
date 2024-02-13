from noknow.core import ZK, ZKSignature, ZKParameters, ZKData, ZKProof
from app import app

def create_server_signature():
    '''
    Server creates its own signature to later verifiy that token sent back by the client has not been tampered with.
    '''
    server_zk = ZK.new(curve_name="secp384r1", hash_alg="sha3_512")
    server_signature: ZKSignature = server_zk.create_signature(app.zk_password)
    return server_zk, server_signature

def create_zk_instance(client_signature):
    '''
    Server uses the client signature to create a zero-knowledge instance.
    '''
    client_zk = ZK(client_signature.params)
    return client_zk

def send_random_token(server_zk, client_zk):
    '''
    Server sends random token to client.
    '''
    token = server_zk.sign(app.zk_password, client_zk.token())
    token = token.dump(separator=":")
    return token

def process_proof(proof, server_zk, server_signature, client_zk, client_signature):
    '''
    The proof sent by the client is verified by the server.
    '''
    proof_recieved = ZKData.load(proof)
    token = ZKData.load(proof_recieved.data, ":")
    if not server_zk.verify(token, server_signature):
        return "Unautorized."
    else:
        return client_zk.verify(proof_recieved, client_signature, data=token)