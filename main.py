from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.fernet import Fernet
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

key = Fernet.generate_key()
cipher_suite = Fernet(key)

class DataModel(BaseModel):
    data: str

# This will hold the encrypted data temporarily for demo purposes.
encrypted_storage = []

@app.post("/encrypt")
def encrypt_data(item: DataModel):
    encrypted_data = cipher_suite.encrypt(item.data.encode())
    encrypted_storage.append(encrypted_data)
    return {"encrypted_data": encrypted_data.decode()}

@app.get("/decrypt")
def decrypt_data():
    if not encrypted_storage:
        raise HTTPException(status_code=404, detail="No data available to decrypt.")
    decrypted_data_list = [cipher_suite.decrypt(data).decode() for data in encrypted_storage]
    encrypted_storage.clear()  # Clear temporary data after decryption
    return {"decrypted_data": decrypted_data_list}

# New route to fetch all encrypted data (this will persist after page reload)
@app.get("/get_all_encrypted")
def get_all_encrypted():
    return {"encrypted_data": [e.decode() for e in encrypted_storage]}
