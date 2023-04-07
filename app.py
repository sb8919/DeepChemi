from flask import Flask, render_template, request, url_for
import algorithm

app = Flask(__name__)

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/show_el')
def show_element():
    element = request.args.get('element')
    el_length = algorithm.bondInfo(element)
    print(element)
    return render_template('show_element.html',element= element, el_length = el_length)

@app.route('/<element_list>,<ele_condition>')
def convert(element_list,ele_condition): # ele_condition -> algorihtm.py -> 원소개수 파라미터 ,el_list -> 들어오는 원소 리스트 =>algorithm.py에서 input_element 값으로 들어감
    try:
        el_list = element_list.split(',')
        output = algorithm.start(el_list)
        print(output)
        if (len(output) >= 1):
            return render_template('index.html', elements = output, input = el_list)
        else:
            return render_template('error.html')
    except:
        return render_template('error.html')
    
@app.route('/dev')
def dev():
    return render_template('test.html')

if __name__ =='__main__':
    app.run(host='0.0.0.0',port=3000, debug = True)