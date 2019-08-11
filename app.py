# coding: UTF-8
from flask import Flask, request, render_template
from get_alg import GetAlg, MyAlg
import pandas as pd
import numpy as np
import random
from solver import State, AlgState, CubeString
import itertools

N_EDGE_TARGET = 22
EDGE_NUMBARING = {'UR': 'え', 'UB': 'う', 'UL': 'い', 'FR': 'け', 'FD': 'ら', 'FL': 'か', 'RU': 'て', 'RB': 'ぬ',
                  'RD': 'れ', 'RF': 'ね', 'LU': 'ち', 'LF': 'な', 'LD': 'り', 'LB': 'に', 'BU': 'つ', 'BR': 'く',
                  'BD': 'る', 'BL': 'き', 'DF': 'さ', 'DR': 'せ', 'DB': 'す', 'DL': 'し'}

app = Flask(__name__)


@app.route('/', methods=['GET'])
def render_form():
    return render_template('register.html')


@app.route('/scramble', methods=["GET"])
def show_scramble():
    alg_state_obj = AlgState('UF', 'ULB', State)
    edge_targets = alg_state_obj.edge_target_cnd
    edge_targets.sort()
    edge_target_block = np.array_split(edge_targets[::-1], N_EDGE_TARGET)
    key = []
    for target in edge_target_block:
        key.append(target[0][:2])
    target_dict = dict(zip(key, edge_target_block))
    if request.method == 'GET':
        return render_template('scramble.html', targets=target_dict)


@app.route('/scramble/result', methods=["POST"])
def scramble():
    alg_state_obj = AlgState('UF', 'ULB', State)
    scramble_list = []
    if request.method == 'POST':
        target_list = request.form.getlist('target')
        n_scramble = request.form['num_scramble']
        for i in range(int(n_scramble)):
            targets = select_target(target_list)
            state = alg_state_obj.get_multi_alg_state(targets)
            cube_string_obj = CubeString(state)
            scramble = cube_string_obj.scramble
            scramble_list.append(scramble)
        return render_template('show_scramble.html', scrambles=np.unique(scramble_list))


def select_target(target_list):
    used_target_list = []
    return_target_list = []
    random.shuffle(target_list)
    for target in target_list:
        print(target)
        target1, target2 = target.split('-')
        ng_list = [target1, target1[::-1], target2, target2[::-1]]
        if np.in1d(np.array(ng_list), np.array(used_target_list)).sum() == 0:
            return_target_list.append(target)
            if len(return_target_list) == 5:
                break
        used_target_list.extend(ng_list)
    return return_target_list


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
            numberings = make_numbering(return_dic)
            return render_template('all_alg.html', all_alg=return_dic,  numberings=numberings)
        numberings = make_numbering(all_alg)
        return render_template('all_alg.html', all_alg=all_alg,  numberings=numberings)
    else:
        if request.form['stickers'] and request.form['register1'] and request.form['register2']:
            stickers = request.form['stickers']
            first_sticker, second_sticker = stickers.split('-')
            register_alg1 = request.form['register1']
            register_alg2 = request.form['register2']
            my_alg_obj = MyAlg(first_sticker, second_sticker, register_alg1, register_alg2)
            all_alg = my_alg_obj.my_alg_dic
            numberings = make_numbering(all_alg)
            return render_template('all_alg.html', all_alg=all_alg, numberings=numberings)
        else:
            return render_template('show_alg.html')


def make_numbering(all_alg_dict):
    keys = all_alg_dict.keys()
    number_list = []
    for key in keys:
        sticker1, sticker2 = key.split('-')
        first_str = EDGE_NUMBARING[sticker1]
        second_str = EDGE_NUMBARING[sticker2]
        number_list.append(first_str + second_str)
    return number_list


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True)
