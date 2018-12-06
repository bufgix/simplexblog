import os, secrets
from PIL import Image

from simplex import app


def save_image(form_pic, _type=None):
    _, file_ext  = os.path.splitext(form_pic.filename)
    file_fn = secrets.token_hex(8) + file_ext
    if _type == 'profile':
        picture_path = os.path.join(app.root_path, 'static', 'profile_pics', file_fn)
        img = Image.open(form_pic)
        img.thumbnail((125, 125))
        img.save(picture_path)
    else:
        picture_path = os.path.join(app.root_path, 'static', 'post_pics', file_fn)
        img = Image.open(form_pic)
        img.thumbnail((520, 350))
        img.save(picture_path)

    return file_fn
