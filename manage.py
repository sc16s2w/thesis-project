# coding:utf8
from flask_ckeditor import CKEditor

from app import app

if __name__ == "__main__":
    ckeditor = CKEditor(app)
    app.run(debug=True)

