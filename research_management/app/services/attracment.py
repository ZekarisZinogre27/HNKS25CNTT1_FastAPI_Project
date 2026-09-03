import os
import uuid
from datetime import datetime

UPLOAD_DIR = "./storage/uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def process_file_upload(file_name_from_user, file_binary_data):
    name_without_ext, file_extension = os.path.splitext(file_name_from_user)
    file_extension = file_extension.lower()
    unique_id = str(uuid.uuid4())
    new_file_name = f"{unique_id}{file_extension}"
    full_storage_path = os.path.join(UPLOAD_DIR, new_file_name)

    with open(full_storage_path, "wb") as f:
        f.write(file_binary_data)

    db_record = {
        "file_uuid": unique_id,
        "original_name": file_name_from_user,
        "file_extension": file_extension,
        "file_size": len(file_binary_data),
        "storage_path": full_storage_path,
        "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return db_record