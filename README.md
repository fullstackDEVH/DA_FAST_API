1 : pip install poetry

2 : poetry init

3 : poetry install -> create/update poetry.lock

4 : poetry config virtualenvs.in-project true
    thiết lập môi trường ảo Python được tạo bên trong thư mục dự án 
     chứ không phải nằm ngoài dự án, mặc đinh là true (gõ poetry env info để thấy đường dẫn thiết lập)
	
5 : poetry install : sau khi xoá và thiết lập lại .venv ở trong dự án thì install lại

6 : poetry shell : chạy môi trường ảo. nhập lệnh exit để thoát môi trường ảo

poetry add library_name : thêm
poetry remove library_name : xoá




<!-- setup alembic  -->

1 : alembic init alembic

setup file alembic/env và alembic.ini
 - alembic/env
  + from app.database import Base
  + target_metadata = Base.metadata
 - alembic.ini
  + sqlalchemy.url = postgresql://postgres:postgres@localhost:5432/DoAn_Apartment

<!-- tạo phiên bản mới khi chỉnh sửa table -->
2 : alembic revision --autogenerate -m "Mô tả thay đổi"

<!-- áp dụng phiên bản mới -->
3 : alembic upgrade head 


<!-- https://app.diagrams.net/#G1LL5jAam8OHK5vP2QU8H8xnODZpZtI_nP -->
<!-- https://github.com/Sanjeev-Thiyagarajan/fastapi-course/blob/main/app/routers/post.py -->
<!-- https://github.com/jmoussa/chat-app-be/blob/develop/app.py -->