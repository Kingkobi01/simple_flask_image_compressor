import os
from flask import Flask, render_template, url_for, send_from_directory
from flask_uploads import IMAGES, UploadSet, configure_uploads, configure_uploads
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from PIL import Image

app = Flask(__name__)

app.config["SECRET_KEY"] = "secretKey"
app.config["UPLOADED_PHOTOS_DEST"] = "uploads"

photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)


class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, "Only images are allowed"),
            FileRequired("Field should not be empty"),
        ]
    )

    submit = SubmitField(label="Upload & Compress")


def compress_image(image):
    img = Image.open(image)
    img = img.convert("RGB")
    compressed_image = os.path.join(
        app.config["UPLOADED_PHOTOS_DEST"], "compressed.jpg"
    )
    img.save(compressed_image, optimize=True, quality=10)
    print(compressed_image)
    return compressed_image


@app.route("/upload/<filename>")
def get_file(filename):
    return send_from_directory(app.config["UPLOADED_PHOTOS_DEST"], filename)


@app.route("/", methods=["GET", "POST"])
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        # filename = photos.save(form.photo.data)
        filename = compress_image(form.photo.data)
        file_url = url_for("get_file", filename="compressed.jpg")
    else:
        file_url = None
        print("Not Validated")

    return render_template("index.html", form=form, file_url=file_url)


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOADED_PHOTOS_DEST"]):
        os.makedirs(app.config["UPLOADED_PHOTOS_DEST"])
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)
