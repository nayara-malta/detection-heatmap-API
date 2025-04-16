import re
from typing import List, Tuple, Any

class DetectionExtractor:
    """
    Classe utilitária para extrair pontos centrais de detecções a partir de dados estruturados.
    """
    @staticmethod
    def extract_points(data: Any, object_name: str, field_name: str = 'deepstream-msg') -> List[Tuple[int, int]]:
        """
        Extrai os pontos centrais das detecções de um objeto específico dentro dos dados fornecidos.

        A função busca recursivamente por um campo específico nos dados, itera sobre as detecções encontradas,
        filtra aquelas que contêm o nome do objeto desejado, extrai as informações da caixa delimitadora
        e calcula o centroide de cada caixa.

        Args:
            data (Any): A estrutura de dados contendo as informações de detecção (pode ser um dicionário, lista, etc.).
            object_name (str): O nome do objeto de interesse para o qual os pontos centrais devem ser extraídos.
            field_name (str, optional): O nome do campo dentro dos dados onde as informações de detecção estão localizadas.
                                         Padrão para 'deepstream-msg'.

        Returns:
            List[Tuple[int, int]]: Uma lista de tuplas, onde cada tupla representa as coordenadas (x, y) do centroide
                                   de uma detecção do objeto especificado. Retorna uma lista vazia se nenhuma detecção
                                   for encontrada para o objeto especificado.
        """
        detections = DetectionExtractor._buscar_campo(data, field_name)
        pontos = []
        for sublista in detections:
            for item in sublista:
                if object_name in item:
                    box = DetectionExtractor._extract_info(item)
                    if box:
                        centroide = DetectionExtractor._calcular_centroide(*box)
                        pontos.append(centroide)
        return pontos

    @staticmethod
    def _buscar_campo(data: Any, nome_campo: str) -> List:
        """
        Busca recursivamente por um campo específico dentro de uma estrutura de dados aninhada.

        Args:
            data (Any): A estrutura de dados a ser pesquisada (pode ser um dicionário, lista, etc.).
            nome_campo (str): O nome do campo a ser procurado.

        Returns:
            List: Uma lista contendo todos os valores encontrados para o campo especificado.
                  Retorna uma lista vazia se o campo não for encontrado.
        """
        valores_encontrados = []

        def buscar_recursivamente(d):
            if isinstance(d, dict):
                for k, v in d.items():
                    if k == nome_campo:
                        valores_encontrados.append(v)
                    elif isinstance(v, (dict, list)):
                        buscar_recursivamente(v)
            elif isinstance(d, list):
                for item in d:
                    buscar_recursivamente(item)

        buscar_recursivamente(data)
        return valores_encontrados

    @staticmethod
    def _extract_info(string: str):
        """
        Extrai informações da caixa delimitadora de uma string formatada.

        A string deve seguir o padrão: 'ID|xmin|ymin|xmax|ymax|classe|confianca'.
        Esta função extrai e retorna as coordenadas xmin, ymin, xmax e ymax como floats.

        Args:
            string (str): A string contendo as informações da detecção.

        Returns:
            tuple[float, float, float, float] | None: Uma tupla contendo (xmin, ymin, xmax, ymax) como floats,
                                                     ou None se a string não corresponder ao padrão esperado.
        """
        padrao = r"(\d+)\|(\d+\.?\d*)\|(\d+\.?\d*)\|(\d+\.?\d*)\|(\d+\.?\d*)\|(\w+)\|(\w+)"
        match = re.match(padrao, string)
        if match:
            return tuple(map(float, match.groups()[1:5]))
        return None

    @staticmethod
    def _calcular_centroide(xmin, ymin, xmax, ymax):
        """
        Calcula as coordenadas do centroide de uma caixa delimitadora.

        Args:
            xmin (float): Coordenada x mínima da caixa.
            ymin (float): Coordenada y mínima da caixa.
            xmax (float): Coordenada x máxima da caixa.
            ymax (float): Coordenada y máxima da caixa.

        Returns:
            tuple[int, int]: Uma tupla contendo as coordenadas inteiras (x, y) do centroide.
        """
        return int((xmin + xmax) / 2), int((ymin + ymax) / 2)