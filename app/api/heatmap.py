from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from app.services.image_handler import ImageHandler
from app.services.detection_extractor import DetectionExtractor
from app.services.heatmapper import Heatmapper
from app.utils.helpers import save_image

router = APIRouter()

class HeatmapRequest(BaseModel):
    """
    Modelo Pydantic para definir o corpo da requisição para gerar um heatmap.
    """
    data_json: dict
    object_wanted: str
    url_image: str


@router.post("/generate-heatmap")
def generate_heatmap(payload: HeatmapRequest):
    """
    Gera um heatmap com base nos dados de detecção fornecidos e o sobrepõe a uma imagem.

    Este endpoint recebe um JSON contendo dados de detecção, o nome do objeto de interesse
    e a URL de uma imagem. Ele processa os dados para extrair os pontos de detecção,
    gera um heatmap com base nesses pontos e o combina com a imagem fornecida.
    A imagem resultante com o heatmap sobreposto é salva e o caminho do arquivo é retornado.

    Args:
        payload (HeatmapRequest): Um objeto Pydantic contendo os dados JSON de detecção,
                                  o nome do objeto desejado e a URL da imagem base.

    Returns:
        dict: Um dicionário JSON contendo o status da operação ('success') e o caminho
              para a imagem gerada ('image_path').

    Raises:
        HTTPException (status_code=500): Se ocorrer algum erro durante o processamento
                                         da imagem, extração de pontos ou geração do heatmap.
    """
    try:
        # Importar imagem
        image_handler = ImageHandler()
        image = image_handler.import_img_url(payload.url_image)

        # Extrair pontos
        extractor = DetectionExtractor()
        detections = extractor.extract_points(
            payload.data_json, payload.object_wanted, field_name="deepstream-msg"
        )

        # Gerar heatmap
        heatmapper = Heatmapper()
        heatmap_image = heatmapper.heatmap_on_img(detections, image)

        # Salvar imagem
        image_path = save_image(heatmap_image)

        return {"status": "success", "image_path": image_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))