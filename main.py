from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.fernet import Fernet
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev purposes; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

key = Fernet.generate_key()
cipher_suite = Fernet(key)

class DataModel(BaseModel):
    data: str

# Permanent encrypted storage (acts like a "database")
permanent_storage = []

@app.post("/encrypt")
def encrypt_data(item: DataModel):
    encrypted_data = cipher_suite.encrypt(item.data.encode())
    permanent_storage.append(encrypted_data)
    return {"encrypted_data": encrypted_data.decode()}

@app.get("/decrypt")
def decrypt():
    if not permanent_storage:
        raise HTTPException(status_code=404, detail="No data available to decrypt.")

    # Temporary decrypted data (will exist per call)
    decrypted_data_list = [cipher_suite.decrypt(data).decode() for data in permanent_storage]
    return {
        "decrypted_data": decrypted_data_list,
        "message": "Decryption successful"
    }
