from PIL import Image
import os
import platform

def _img_to_opacity(img: Image.Image, opacity: float) -> Image.Image:
    """
    Aplica um fator de opacidade ao canal alfa de uma imagem.

    Args:
        img: O objeto PIL Image de entrada.
        opacity: Um valor float entre 0.0 e 1.0 representando a opacidade desejada.
                 0.0 é totalmente transparente e 1.0 é totalmente opaco.

    Returns:
        Um novo objeto PIL Image com o canal alfa ajustado.
    """
    img = img.convert('RGBA')
    alpha = img.split()[3]
    alpha = alpha.point(lambda p: int(p * opacity))
    img.putalpha(alpha)
    return img

def save_image(image: Image.Image) -> str | None:
    """
    Salva uma imagem PIL em um diretório padrão com base no sistema operacional.

    No Windows, a imagem é salva em '~/results_api'.
    Em outros sistemas (como Linux), a imagem é salva em '/tmp/results_api'.
    Se o diretório não existir, ele será criado.

    Args:
        image: O objeto PIL Image a ser salvo.

    Returns:
        O caminho completo para o arquivo de imagem salvo como uma string,
        ou None se ocorrer um erro durante o salvamento.
    """
    system = platform.system()
    if system == "Windows":
        directory = os.path.join(os.environ['USERPROFILE'], "results_api")
    else:
        directory = "/tmp/results_api"

    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, f"heatmap.png")
    try:
        image.save(file_path)
        return file_path
    except Exception as e:
        print(f"Erro ao salvar a imagem em '{file_path}': {e}")
        return None