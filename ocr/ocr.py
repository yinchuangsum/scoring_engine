import os

from PIL.Image import Image
from pdf2image import convert_from_path
from pytesseract import pytesseract, Output
from sqlalchemy.orm import sessionmaker

from db import File, Page


class Ocr:
    def __init__(self, path, output_folder, engine):
        self.path = path
        self.output_folder = output_folder
        self.tmp_file = "tmp.jpeg"
        self.session_maker = sessionmaker()
        self.session_maker.configure(bind=engine)

    def run(self):
        # save to file db
        session = self.session_maker()
        file = File(file_path=self.path, folder_location=self.output_folder)
        session.add(file)
        session.flush()
        images = self.pdf_to_images()
        for idx, image in enumerate(images):
            page = idx + 1
            orientation = self.detect_orientation(image)
            image = self.rotate_image(image, orientation)
            txt = self.image_to_txt(image)
            file_path = self.save_file(txt, page)
            # save to page db
            page_object = Page(file_id=file.id, page=page, orientation=orientation, file_path=file_path)
            session.add(page_object)
            session.flush()
        session.commit()
        session.close()

    def pdf_to_images(self):
        return convert_from_path(self.path)

    def save_image_to_tmp(self, image):
        return Image.save(image, self.tmp_file)

    def image_to_txt(self, image):
        return pytesseract.image_to_string(image)

    def detect_orientation(self, image):
        self.save_image_to_tmp(image)
        data = pytesseract.image_to_osd(self.tmp_file, output_type=Output.DICT)
        return data["rotate"]

    def rotate_image(self, image, angle):
        return image.rotate(360 - angle, expand=1)

    def save_file(self, txt, page):
        file_name = f"{page}.txt"
        file_path = os.path.join(self.output_folder, file_name)
        f = open(file_path, "w", encoding="utf-8")
        f.write(txt)
        f.close()
        return os.path.abspath(file_path)
