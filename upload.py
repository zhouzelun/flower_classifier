import os
from flask import Flask, request, url_for, send_from_directory
from werkzeug import secure_filename
import flowers_application
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','JPG'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()+'/picture'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ref = {}
ref[0]='雏菊'
ref[1]='蒲公英'
ref[2]='玫瑰'
ref[3]='向日葵'
ref[4]='郁金香'
html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>Photo Upload</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=upload>
    </form>
    '''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    
@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
    
    
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_url = url_for('uploaded_file', filename=filename)
            img_path = app.config['UPLOAD_FOLDER']+file_url
            index = flowers_application.classifier(img_path)
            return html + '<br><img src=' + file_url + ' width="200" height="200"><p>这是:'+ref[index]+'</p>'
    return html


if __name__ == '__main__':
    app.run()
    