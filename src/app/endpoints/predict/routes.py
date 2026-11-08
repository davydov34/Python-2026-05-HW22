import numpy as np
from fastapi import APIRouter, Depends, HTTPException

from src.app.common_entities import InputDataONNX, OutputDataONNX, UserResponse
from src.app.endpoints.auth.logic import Role, RoleChacker
from src.app.logger_app.app_logger import logger as to_log
from src.app.onnx.inference import input_name, session

router = APIRouter(prefix="/predict", tags=["predict"])

allowed_role = RoleChacker([Role.ADMIN, Role.USER])


@router.post("")
def predict(input_data: InputDataONNX, p: UserResponse = Depends(allowed_role)):
    if session is None:
        raise HTTPException(status_code=500, detail="Модель не была загружена")

    source_data = np.array(
        [input_data.Pregnancies, input_data.Glucose, input_data.BMI, input_data.Age],
        dtype=np.float32,
    ).reshape(1, -1)

    try:
        output = session.run(None, {input_name: source_data})
        raw_pred = OutputDataONNX(output[0].tolist())

        to_log.info("Получен результат инференса")
    except:
        to_log.error("Ошибка инференса")
        raise HTTPException(status_code=500, detail="Ошибка инференса")

    return raw_pred.get_value()
