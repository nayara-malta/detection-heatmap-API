from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from PIL import Image
# from app.services.grey_heatmapper import PILGreyHeatmapper
from app.utils.helpers import _img_to_opacity
from abc import ABC, abstractmethod

class Heatmapper:
    """
    Gera um heatmap colorido sobre uma imagem base, com base em pontos de detecção.
    """
    def __init__(self, point_diameter=100, point_strength=0.1, opacity=0.75, colour_scheme='default'):
        """
        Inicializa o Heatmapper.

        Args:
            point_diameter (int): Diâmetro de cada ponto de detecção no heatmap.
            point_strength (float): Intensidade de cada ponto de detecção (afeta a opacidade do ponto).
            opacity (float): Opacidade geral da camada do heatmap sobre a imagem base.
            colour_scheme (str): Esquema de cores a ser usado para o heatmap. Atualmente, apenas 'default' é suportado.
        """
        self.opacity = opacity
        self.grey_heatmapper = PILGreyHeatmapper(point_diameter, point_strength)
        self._cmap = self._load_colormap(colour_scheme)

    def _load_colormap(self, scheme):
        """
        Carrega o colormap a partir de um arquivo de imagem.

        Args:
            scheme (str): O nome do esquema de cores. Atualmente, apenas 'default' é suportado.

        Returns:
            matplotlib.colors.LinearSegmentedColormap: O colormap carregado.
        """
        path = 'app/assets/default.png'
        img = Image.open(path).resize((256, 1))
        colours = [tuple(c/255 for c in img.getpixel((x, 0))) for x in range(256)]
        return LinearSegmentedColormap.from_list('custom_cmap', colours)

    def heatmap_on_img(self, points, base_img):
        """
        Gera e sobrepõe um heatmap colorido sobre uma imagem base.

        Args:
            points (list): Uma lista de tuplas (x, y) representando as coordenadas dos pontos de detecção.
            base_img (PIL.Image.Image): A imagem base sobre a qual o heatmap será sobreposto.

        Returns:
            PIL.Image.Image: Uma nova imagem com o heatmap colorido sobreposto.
        """
        width, height = base_img.size
        heat = self.grey_heatmapper.heatmap(width, height, points)
        heat_coloured = self._cmap(np.array(heat), bytes=True)
        heat_image = Image.fromarray(heat_coloured)
        heat_opacity = _img_to_opacity(heat_image, self.opacity)
        return Image.alpha_composite(base_img.convert('RGBA'), heat_opacity)


class GreyHeatMapper(ABC):
    """
    Classe abstrata para gerar um heatmap em escala de cinza.
    """
    def __init__(self, point_diameter: int, point_strength: float):
        """
        Inicializa o GreyHeatMapper.

        Args:
            point_diameter (int): Diâmetro dos pontos no heatmap em escala de cinza.
            point_strength (float): Intensidade dos pontos no heatmap em escala de cinza (afeta a opacidade).
        """
        self.point_diameter = point_diameter
        self.point_strength = point_strength

    @abstractmethod
    def heatmap(self, width: int, height: int, points: list) -> Image.Image:
        """
        Método abstrato para gerar o heatmap em escala de cinza.

        Args:
            width (int): Largura da imagem do heatmap.
            height (int): Altura da imagem do heatmap.
            points (list): Uma lista de tuplas (x, y) representando as coordenadas dos pontos de detecção.

        Returns:
            PIL.Image.Image: Uma imagem em escala de cinza representando o heatmap.
        """
        pass


class PILGreyHeatmapper(GreyHeatMapper):
    """
    Implementação do GreyHeatMapper usando a biblioteca PIL para gerar o heatmap em escala de cinza.
    """
    def __init__(self, point_diameter: int, point_strength: float):
        """
        Inicializa o PILGreyHeatmapper.

        Args:
            point_diameter (int): Diâmetro dos pontos no heatmap em escala de cinza.
            point_strength (float): Intensidade dos pontos no heatmap em escala de cinza (afeta a opacidade).
        """
        super().__init__(point_diameter, point_strength)

    def heatmap(self, width: int, height: int, points: list) -> Image.Image:
        """
        Gera um heatmap em escala de cinza usando a biblioteca PIL.

        Args:
            width (int): Largura da imagem do heatmap.
            height (int): Altura da imagem do heatmap.
            points (list): Uma lista de tuplas (x, y) representando as coordenadas dos pontos de detecção.

        Returns:
            PIL.Image.Image: Uma imagem em escala de cinza representando o heatmap.
        """
        heat = Image.new('L', (width, height), color=255)

        dot = (
            Image.open('app/assets/450pxdot.png')
            .copy()
            .resize((self.point_diameter, self.point_diameter), resample=Image.LANCZOS)
        )
        dot = _img_to_opacity(dot, self.point_strength)

        for x, y in points:
            x = int(x - self.point_diameter / 2)
            y = int(y - self.point_diameter / 2)
            heat.paste(dot, (x, y), dot)

        return heat