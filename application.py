import os
import subprocess
import filecmp

from flask import Flask
from flask import render_template, request, url_for, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MY_SECRET_KEY'


@app.route('/')
def index_page():
    return render_template('index.html')


def compile_code(name: str, tc: str):
    display_str = "Compiled Successfully "
    cmd1 = ['g++', 'code_file/'+name, '-o', 'exec_file/exec.out']
    compiler_out = subprocess.Popen(cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = compiler_out.communicate()

    if compiler_out.returncode == 0:
        try:

            cmd2 = './exec_file' + '/exec.out <test_input/input' + tc + '.txt >code_output/output' + tc + '.txt'
            print(cmd2)
            str2 = subprocess.check_output(cmd2, shell=True)
            # str2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # a2, a3 = str2.communicate()
            # print(str2)
            # print(a2, a3)
            # print("after all")
        except subprocess.TimeoutExpired:
            print("TimeLimit Exceed")
            display_str += " <br> Time Limit exceeds"
        except:
            pass
        print(display_str)
        return True, display_str
    else:
        return False, e.decode('utf-8')


@app.route('/successful_upload')
def successful_upload():
    r, compiler_output = compile_code("code1.cpp", "1")
    # cmd3 = 'cmp ref_out1.txt output1.txt'
    a = False
    if r is True:
        try:
            # str3 = subprocess.check_output(cmd3, shell=True)
            a = filecmp.cmp('test_output/ref_out1.txt', 'code_output/output1.txt')
            # print("result: " + str3.decode("utf-8"))
            # print(str3.split()[2])
        except:
            print("error  ooo")

    return "successfully uploaded <br><br><br>" + \
           "Compiler ouput <br>" + \
           compiler_output + \
           "<br><br><br>test case 1: " + str(a)
    # + str(str1) +str(str2)+str(str3)


@app.route("/handleUpload", methods=['POST'])
def handleFileUpload():
    if 'code1' in request.files:
        data_file = request.files['code1']
        if data_file.filename != '':
            print(os.getcwd())
            data_file.save(os.path.join(os.getcwd() + '/code_file', data_file.filename))
        return redirect(url_for('successful_upload'))
    return "error uploading"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
