import os

auto_data = os.path.split(os.path.realpath(__file__))[0]

auto = os.path.dirname(auto_data)

LOG_PATH = os.path.join(auto, "log") + r"\\"
ERROR_IMAGE_PATH = os.path.join(auto, "error_image")+ r"\\"
HOST_PATH = os.path.join(auto, "conf", "host.ini")
MYSQL_PATH = os.path.join(auto, "conf", "mysql.ini")
USER_PATH = os.path.join(auto, "conf", "user.ini")
PYTEST_PATH = os.path.join(auto, "pytest.ini")


base_url = "https://www.baidu.com/"
op_username = ""
op_password = ""

login_path = ""
homepage_module_path = ""
main_module_path = ""

base_driver = []
