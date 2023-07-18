from tempfile import mkdtemp

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from src.utils.environ import is_docker
from src.utils.my_logger import MyLogger

logger = MyLogger(__name__)


@logger.logging_function(with_return=False)
def get_mac_chrome_driver(*, dir_download: str) -> WebDriver:
    options = Options()
    options.add_experimental_option(
        "prefs", {"download.default_directory": dir_download}
    )

    return WebDriver(service=Service(ChromeDriverManager().install()), options=options)


@logger.logging_function(with_return=False)
def get_docker_chrome_driver(*, dir_download: str) -> WebDriver:
    options = Options()

    options.binary_location = "/opt/chrome/chrome"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")
    options.add_experimental_option(
        "prefs", {"download.default_directory": dir_download}
    )
    return WebDriver(options=options, service=Service(executable_path="/opt/chromedriver"))


@logger.logging_function(with_return=False)
def get_chrome_driver(*, dir_download: str) -> WebDriver:
    if is_docker():
        return get_docker_chrome_driver(dir_download=dir_download)
    else:
        return get_mac_chrome_driver(dir_download=dir_download)