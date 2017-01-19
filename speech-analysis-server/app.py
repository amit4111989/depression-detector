from flask import Flask, render_template
from flask import request
from flask import jsonify
import sys
import os
from calculate_data import calculate_data
import json

app = Flask(__name__)


@app.route('/recording', methods=['POST'])
def alexa_task():
    file = request.files['file']
    filename = str(file.filename)
    file.save('current_data/' + file.filename)
    reply = {'msg': 'Success'}
    sox_command = 'sox -r 16000 -e unsigned -b 16 -c 1 current_data/%s current_data/%s.wav' % (
        filename, filename[:-4])
    os.system(sox_command)
    with open('current_file.text', 'w+') as f:
        f.write(str(filename[:-4]))
    return jsonify({'reply': reply}), 201


@app.route('/textfile', methods=['POST'])
def transcipt():
    data = json.loads(request.data)
    text = str(data['text'])
    text = text.upper()
    with open('current_file.text', 'r') as f:
        filename = f.read()
    with open('/tmp/random_folder/' + filename + '.lab', 'w+') as f:
        f.write(text)
    os.system('mv current_data/%s.wav /tmp/random_folder/' % filename)
    os.system('rm current_data/*')
    result = calculate_data(filename, '/tmp/random_folder')
    os.system('rm /tmp/dexter/*')
    ref_ratio = 111792.7  # ratio for men calculated from average F1/F2 data
    ratio = (result[1] / ref_ratio)
    with open('result.txt', 'w+') as f:
        f.write('%f,%f,%f,%f' % (ratio, result[0]['a'][
                'dur'], result[0]['i']['dur'], result[0]['u']['dur']))
    print result, ratio  # render_template('template.html',f1='10')
    # TODO filter by timestamp
    # TODO create filename for lab file
    # TODO create lab file in the folder with .wav
    # TODO run calculate_data for filename and folder
    # TODO JSONIFY results and send to UI


@app.route('/result', methods=['GET'])
def result():
    with open('result.txt', 'r') as f:
        results = f.read().split(',')
    return render_template('template.html', a_dur=results[1], i_dur=results[2], u_dur=results[3], ratio=results[0])

if __name__ == '__main__':
    app.run()
