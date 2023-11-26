from fastapi import UploadFile, File, HTTPException
import os


def upload_file(
    folder_name: str,
    endpoint_path: str,
    allowed_image_types: dict,
    file_upload: list[UploadFile] = File(...),
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

        return image_path_banner_apartment
    except Exception as error:
        raise HTTPException(status_code=500, detail="Lỗi server")
    finally:
        file_upload.close()


def delete_file_upload(folder_path: str, file_name: str):
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


async def upload_files(
    folder_name: str, allowed_image_types: set, files: list[UploadFile], endpoint: str
):
    try:
        uploaded_images = []
        for index, file_upload in enumerate(files):
            if file_upload.content_type not in allowed_image_types:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported image type: {file_upload.content_type} for file {index + 1}",
                )

            # folder_path = os.path.join(folder_name, str(index))
            # lấy tên folder
            folder_path = os.path.join(folder_name)
            # tạo folder với tên
            os.makedirs(folder_path, exist_ok=True)
            # lấy tên path
            image_path = os.path.join(folder_path, str(index))

            with open(image_path, "wb") as f:
                f.write(file_upload.file.read())

            uploaded_images.append(f"{endpoint}/{str(index)}")
            
        return uploaded_images
    except Exception as error:
        raise HTTPException(status_code=500, detail="Server error")
    finally:
        for file_upload in files:
            file_upload.file.close()
