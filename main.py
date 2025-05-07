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

# Generate a key for encryption and decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Pydantic model to receive data for encryption
class DataModel(BaseModel):
    data: str

# Permanent storage (simulated as an in-memory list for now)
permanent_storage = []

# Temporary storage (this will be stored on the client side)
temporary_storage = []

# Route to encrypt data and store it permanently
@app.post("/encrypt")
def encrypt_data(item: DataModel):
    encrypted_data = cipher_suite.encrypt(item.data.encode())
    permanent_storage.append(encrypted_data)
    return {"encrypted_data": encrypted_data.decode()}

# Route to retrieve decrypted data temporarily
@app.get("/decrypt")
async def decrypt():
    if not permanent_storage:
        raise HTTPException(status_code=404, detail="No data available to decrypt.")
    
    # Decrypt all the stored data and store it temporarily
    temporary_storage.clear()  # Clear the temporary storage before adding new data
    decrypted_data_list = [cipher_suite.decrypt(data).decode() for data in permanent_storage]
    temporary_storage.extend(decrypted_data_list)  # Store in temporary storage
    
    return {"decrypted_data": decrypted_data_list, "message": "Decryption successful"}

