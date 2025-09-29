from django import template
import re

register = template.Library()

@register.filter(name='youtube_embed_url')
def youtube_embed_url(value):
    """
    Transforma una URL de YouTube normal (watch?v=VIDEO_ID)
    a una URL de inserción (embed/VIDEO_ID).
    También maneja URLs cortas (youtu.be/VIDEO_ID).
    """
    if "watch?v=" in value:
        # URL de YouTube normal: https://www.youtube.com/watch?v=VIDEO_ID
        match = re.search(r"watch\?v=([a-zA-Z0-9_-]+)", value)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"
    elif "youtu.be/" in value:
        # URL corta de YouTube: https://youtu.be/VIDEO_ID
        match = re.search(r"youtu.be/([a-zA-Z0-9_-]+)", value)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"
    
    # Si la URL ya es de inserción o no es una URL de YouTube reconocida, la retorna tal cual.
    # Puedes añadir más lógica si tienes otros formatos de URL.
    return value