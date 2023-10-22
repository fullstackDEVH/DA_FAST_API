from fastapi import UploadFile, File, HTTPException
import os


def upload_file(
    folder_name: str,
    endpoint_path: str,
    allowed_image_types: dict,
    file_upload: UploadFile = File(...),
):
    try:
        if file_upload.content_type not in allowed_image_types:
            raise HTTPException(
                status_code=404,
                detail=f"Unsupport image type : {file_upload.content_type}!!",
            )

        folder_banner_apartment = os.path.join(folder_name)
        os.makedirs(folder_banner_apartment, exist_ok=True)

        # Tạo đường dẫn đến tệp ảnh
        image_path_banner_apartment = os.path.join(
            folder_banner_apartment, endpoint_path
        )

        # Lưu tệp ảnh
        with open(image_path_banner_apartment, "wb") as f:
            f.write(file_upload.file.read())

        return f"/apartments/{endpoint_path}/banner"
    except Exception as error:
        raise HTTPException(status_code=500, detail="Lỗi server")
    finally:
        file_upload.close()


def delete_file_upload(folder_path: str, file_name : str):
    folder_banner = os.path.join(folder_path)
    path_banner = os.path.join(folder_banner, file_name)
    
    try:
        # Kiểm tra xem tệp có tồn tại không
        if os.path.exists(path_banner):
            os.remove(path_banner)
        else:
            raise HTTPException(status_code=404, detail="Tệp không tồn tại")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Lỗi server")
