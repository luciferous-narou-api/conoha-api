from src.utils.my_logger import MyLogger
from src.models import ModelGetInformation

logger = MyLogger(__name__)


@logger.logging_function()
def get_information(*, model: ModelGetInformation) -> dict:
    return {"test": 1, "ncode": model.ncode}
