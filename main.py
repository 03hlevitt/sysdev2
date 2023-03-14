from frontend.base_page import orderListForm
from backend.main import Backend

if __name__ == "__main__":
    Backend().init_db()
    orderListForm("menu")
