#!/usr/bin/env python
import os
import pandas as pd
from flask import Flask, request,render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename





# create app
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = '/home/Firiyuu77/mysite/uploads'
app.config['ALLOWED_EXTENSIONS'] = set(['txt','csv','xlsx'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def main():
    return render_template('index.html')

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return redirect(url_for('uploaded_file',
                                filename=filename))

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an csv , that csv  is going to be returned after the eupload then evaluation.
@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    if __name__ == '__main__':
      app.run(
      host="0.0.0.0",
      port=int("80"),
      debug=True
         )
    pathto_csv = os.path.join('mysite/uploads/',filename)
    #filename = os.path.abspath(dire)
    if request.method == 'GET':
        # show html form
       return render_template('formcsv.html')
    elif request.method == 'POST':
        # calculate result
       data_df = pd.read_csv(pathto_csv)
       data_df['Forecasted Values:']=0


       m1 = request.form.get('m1')
       m2 = request.form.get('m2')


       for i, row in data_df.iterrows() :
          rem = data_df.iloc[i]['Current SOH']
          sold1 = data_df.iloc[i][m1]
          sold2 = data_df.iloc[i][m2]

          rem = int(rem)
          sold1 = int(sold1)
          sold2 = int(sold2)
          result = forecast(rem,sold1,sold2)

          data_df.set_value([i], ['Forecasted Values:'], result)

       data_df.to_csv(pathto_csv)

       path = os.path.join(app.root_path, 'uploads')
       assert os.path.exists (path)
       return send_from_directory (path, filename)




#--------------------------------------------------------

#--------------------------------------------------------

#--------------------------------------------------------UNFINISHED PART




#--------------------------------------------------------
#
#
#
#
# ------------------------------------------------------------
# MAIN Program
# ------------------------------------------------------------



#------------------------------------------------------------------------------------------------







def calculate(r,t,l):
    return ((l+t)/2)*3


def forecast(rem, sold1, sold2):


     if (rem == 0 and sold1 == 0 and sold2 ==0): #All ZERO
         return 15
     elif (rem == 0 and sold1 == 0 and sold2 < 10): #ALL FOR ONE PRODUCT VALUE
         return sold2*3
     elif (rem == 0 and sold1 < 10 and sold2 ==0):
         return sold1*3
     elif (rem < 10 and sold1 == 0 and sold2 == 0):
         return rem*3
     #END FOR ONE PRODUCT VALUE
     elif (rem>= 10 and  sold1>=10 and sold2>=10):

          if((rem/3)>=(sold1+10) or (rem/3)>=(sold1+10)):
              return 0
          else:
              return calculate(rem,sold1,sold2)-rem
     elif (rem<10 and sold1<10 and sold2<10):
         return calculate(rem,sold1,sold2)
     elif (rem == 0 and sold1>=10 and sold2>=10):
         return calculate(rem,sold1,sold2)
     else:
         return sold1






@app.route('/forecaster', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # show html form
        return render_template('formmanual.html')
    elif request.method == 'POST':
        # calculate result
        rem = int(request.form.get('remaining'))
        sold1 = int(request.form.get('sold1'))
        sold2 = int(request.form.get('sold2'))

        result = forecast(rem,sold1,sold2)

        return '<h1>Result: %s</h1>' % result



if __name__ == "__main__":
    app.run(debug=True)


