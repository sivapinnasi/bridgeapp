from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.fernet import Fernet
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://fbridge.netlify.app"],  # Replace "*" with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Generate a key for encryption and decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Pydantic model to receive data for encryption
class DataModel(BaseModel):
    data: str

# Store encrypted data
encrypted_storage = []

# Route to encrypt data
@app.post("/encrypt")
def encrypt_data(item: DataModel):
    encrypted_data = cipher_suite.encrypt(item.data.encode())
    encrypted_storage.append(encrypted_data)
    return {"encrypted_data": encrypted_data.decode()}

# Route to decrypt data
@app.get("/decrypt")
async def decrypt():
    if not encrypted_storage:
        raise HTTPException(status_code=404, detail="No data available to decrypt.")
    
    # Decrypt all the stored data
    decrypted_data_list = [cipher_suite.decrypt(data).decode() for data in encrypted_storage]
    
    # Clear the encrypted storage after decryption
    encrypted_storage.clear()
    
    return {"decrypted_data": decrypted_data_list, "message": "Decryption successful"}

