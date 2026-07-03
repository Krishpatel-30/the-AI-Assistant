import os
from google import genai


class ImageChat:

    def __init__(self, client):

        self.client = client

        self.image_path = None

    # ----------------------------

    def load_image(self, path):

        self.image_path = path

    # ----------------------------

    def has_image(self):

        return self.image_path is not None

    # ----------------------------

    def clear(self):

        self.image_path = None