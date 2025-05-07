from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.fernet import Fernet

app = FastAPI()

# Generate a static key (you can replace this with your own key and store securely)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

class DataModel(BaseModel):
    data: str

# Simulated encrypted database
encrypted_storage = []

@app.post("/encrypt")
def encrypt_data(item: DataModel):
    try:
        encrypted_data = cipher_suite.encrypt(item.data.encode())
        encrypted_storage.append(encrypted_data)
        return {"encrypted_data": encrypted_data.decode()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/decrypt")
def decrypt_data():
    try:
        if not encrypted_storage:
            raise HTTPException(status_code=404, detail="No data available to decrypt.")
        decrypted_data_list = [cipher_suite.decrypt(data).decode() for data in encrypted_storage]
        encrypted_storage.clear()  # Simulate emptying virtual DB
        return {"decrypted_data": decrypted_data_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
