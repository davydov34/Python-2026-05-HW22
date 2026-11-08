from pathlib import Path

import onnxruntime as ort

from src.app.logger_app.app_logger import logger as to_log

onnx_file = Path.cwd() / "src/app/onnx/diabetes_model.onnx"

session, input_name = None, None

# Загрузка модели
try:
    session = ort.InferenceSession(str(onnx_file), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    to_log.info("Модель успешно загружена")
except Exception as e:
    to_log.error(f"В процессе загрузки модели произола ошибка: {e}")
    session = None
