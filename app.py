#import libraries for flask
from flask import Flask, render_template, request
from werkzeug import secure_filename
import sys
#import libraries for machine learning
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
#app.config['MAX_CONTENT_LENGTH'] =  1024
#uploadedFilename = "uploadedfile"
uploaddir = "static/"

#todo : move this function to an external file and import
def binarize_array(numpy_array, threshold=200):
    """Binarize a numpy array."""
    for i in range(len(numpy_array)):
        for j in range(len(numpy_array[0])):
            if numpy_array[i][j] > threshold:
                numpy_array[i][j] = 255
            else:
                numpy_array[i][j] = 0
    return numpy_array


@app.route('/')
def index():
   #return "Welcome. please visit "
   return render_template('index.html')


@app.route('/upload')
def upload():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        fname = f.filename
        fnameSecure = secure_filename(fname)
        f.save(uploaddir+fnameSecure)
        print('file type = '+str(type(f)), file=sys.stderr)
        print('uploaddir+fnameSecure = '+uploaddir+fnameSecure, file=sys.stderr)
        #f.save(uploaddir+secure_filename(uploadedFilename))
        image = Image.open(uploaddir+fnameSecure)
        print('type(image) = '+str(type(image)), file=sys.stderr)
        image_L = image.convert('L')
        print('type(image_L) : '+str(type(image_L)), file=sys.stderr)
        print('np.array(image_L).shape : '+str(np.array(image_L).shape), file=sys.stderr)
        image_L_nparray = np.array(image_L)
        image_L.save(uploaddir+'image_L.png')
        image_l28 = image_L.resize((28,28))
        image_l28.save(uploaddir+'image_l28.png')
        image_threshold = binarize_array( np.array(image_l28), 100)
        Image.fromarray(image_threshold).save(uploaddir+'image_threshold.png')
        #print(' : '+str(), file=sys.stderr)
        #return 'file uploaded successfully 7 converted'
        predicted=0
        return render_template('results.html', fname=fname, predicted=predicted)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
