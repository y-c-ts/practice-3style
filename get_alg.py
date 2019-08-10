import pandas as pd
import numpy as np


class GetAlg(object):
    def __init__(self, sticker1, sticker2):
        self.sticker1 = sticker1
        self.sticker2 = sticker2
        self.Jack_df = pd.read_csv('./data/jack.csv', index_col=0)
        self.Graham_df = pd.read_csv('./data/graham.csv', index_col=0)
        self.Daniel_df = pd.read_csv('./data/daniel.csv', index_col=0)
        self.Ishaan_df = pd.read_csv('./data/ishaan.csv', index_col=0)
        self.ishaan_alg = []
        self.daniel_alg = []
        self.jack_alg = []
        self.graham_alg = []

        self.set_all_alg()

    def get_one_alg_from_df(self, df):
        alg1 = df[self.sticker1].loc[self.sticker2]
        alg2 = df[self.sticker2].loc[self.sticker1]
        algs = []
        if alg1 is not np.nan:
            algs.append(alg1)
        if alg2 is not np.nan:
            algs.append(alg2)
        return ' , '.join(algs)

    def set_all_alg(self):
        self.graham_alg = self.get_one_alg_from_df(self.Graham_df)
        self.jack_alg = self.get_one_alg_from_df(self.Jack_df)
        self.daniel_alg = self.get_one_alg_from_df(self.Daniel_df)
        self.ishaan_alg = self.get_one_alg_from_df(self.Ishaan_df)


class MyAlg(object):
    def __init__(self, sticker, inv_sticker, alg1, alg2):
        self.my_df = pd.read_csv('./data/my_df.csv', index_col=0)
        self.alg1 = alg1
        self.alg2 = alg2
        self.sticker = sticker
        self.inv_sticker = inv_sticker
        self.my_alg_dic = {}
        self.set_alg()
        self.my_alg_dic = self.get_register_alg(self.my_df)

    def set_alg(self):
        self.my_df[self.sticker].loc[self.inv_sticker] = self.alg1
        self.my_df[self.inv_sticker].loc[self.sticker] = self.alg2
        self.my_df.to_csv('./data/my_df.csv')

    @staticmethod
    def get_register_alg(df):
        dic = {}
        for column_name, items in df.iteritems():
            items = items.dropna()
            if len(items) > 0:
                for idx, item in items.iteritems():
                    dic[column_name + '-' + idx] = item
        return dict(sorted(dic.items()))








