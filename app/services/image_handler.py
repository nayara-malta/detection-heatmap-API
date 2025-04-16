import requests
from PIL import Image
from io import BytesIO

class ImageHandler:
    @staticmethod
    def import_img_url(url: str) -> Image.Image:
        """
        Importa uma imagem a partir de uma URL do Google Drive.

        Args:
            url (str): URL compartilhável do Google Drive.

        Returns:
            PIL.Image.Image: A imagem carregada.
        """
        file_id = url.split('/')[-2]
        download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))