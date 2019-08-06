from flask import Flask, request, render_template
from get_alg import GetAlg, MyAlg
import pandas as pd
import solver as sv

app = Flask(__name__)
@app.route('/', methods=['GET'])
def render_form():
    cubestring = 'DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL'
    a = sv.solve(cubestring, 20, 2)
    print('----------------------------')
    print(a)
    return render_template('register.html')


@app.route('/register', methods=["POST"])
def show_result():
    if request.form['stickers']:
        stickers = request.form['stickers']
        if '-' in stickers:
            first_sticker, second_sticker = stickers.split('-')
        elif ' ' in stickers:
            first_sticker, second_sticker = stickers.split(' ')
            stickers = first_sticker + '-' + second_sticker
        get_alg_obj = GetAlg(first_sticker, second_sticker)
        my_alg_dic = MyAlg.get_register_alg(pd.read_csv('./data/my_df.csv', index_col=0))
        try:
            my_alg = my_alg_dic[stickers]
        except KeyError:
            my_alg = 'まだ登録してません'
    return render_template('show_alg.html', graham=get_alg_obj.graham_alg, daniel=get_alg_obj.daniel_alg,
                           ishaan=get_alg_obj.ishaan_alg, jack=get_alg_obj.jack_alg, stickers=stickers,
                           stickers_inv=second_sticker + '-' + first_sticker, my_alg=my_alg)


@app.route('/alg', methods=["POST", "GET"])
def register_alg():
    all_alg = MyAlg.get_register_alg(pd.read_csv('./data/my_df.csv', index_col=0))
    if request.method == "GET":
        if request.args.get('search', ''):
            query = request.args.get('search', '')
            return_dic = {}
            for key, value in all_alg.items():
                if query in key:
                    return_dic[key] = value
            return render_template('all_alg.html', all_alg=return_dic)
        return render_template('all_alg.html', all_alg=all_alg)
    else:
        if request.form['stickers'] and request.form['register1'] and request.form['register2']:
            stickers = request.form['stickers']
            first_sticker, second_sticker = stickers.split('-')
            register_alg1 = request.form['register1']
            register_alg2 = request.form['register2']
            my_alg_obj = MyAlg(first_sticker, second_sticker, register_alg1, register_alg2)
            return render_template('all_alg.html', all_alg=my_alg_obj.my_alg_dic)
        else:
            return render_template('show_alg.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True)
