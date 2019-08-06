from kociemba import solve
import numpy as np


class State:
    def __init__(self, cp, co, ep, eo):
        self.cp = np.array(cp, dtype='int8')
        self.co = np.array(co, dtype='int8')
        self.ep = np.array(ep, dtype='int8')
        self.eo = np.array(eo, dtype='int8')

    def apply_move(self, move):
        new_cp = self.cp[move.cp]
        new_co = (self.co[move.cp] + move.co) % 3
        new_ep = self.ep[move.ep]
        new_eo = (self.eo[move.ep] + move.eo) % 2
        return State(new_cp, new_co, new_ep, new_eo)


class CubeString:
    def __init__(self, cube_state):
        self.cube_string = ''
        self.cube_string_dict = {'U5': 'U', 'F5': 'F', 'R5': 'R', 'L5': 'L', 'D5': 'D', 'B5': 'B'}
        self.cube_state = cube_state
        self.edge_place = ['BL', 'BR', 'FR', 'FL', 'UB', 'UR', 'UF', 'UL', 'DB', 'DR', 'DF', 'DL']
        self.corner_place = ['ULB', 'URB', 'URF', 'ULF', 'DLB', 'DRB', 'DRF', 'DLF']
        self.cube_string_edge = [('B6', 'L4'), ('B4', 'R6'), ('F6', 'R4'), ('F4', 'L6'), ('U2', 'B2'), ('U6', 'R2'),
                                 ('U8', 'F2'), ('U4', 'L2'), ('D8', 'B8'), ('D6', 'R8'), ('D2', 'F8'), ('D4', 'L8')]
        self.cube_string_corner = [('U1', 'L1', 'B3'), ('U3', 'B1', 'R3'), ('U9', 'R1', 'F3'), ('U7', 'F1', 'L3'),
                                   ('D7', 'B9', 'L7'), ('D9', 'R9', 'B7'), ('D3', 'F9', 'R7'), ('D1', 'L9', 'F7')]
        self.primary_list = ['U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8', 'U9', 'R1', 'R2', 'R3', 'R4',
                             'R5', 'R6', 'R7', 'R8', 'R9', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8',
                             'F9', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'L1', 'L2', 'L3',
                             'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7',
                             'B8', 'B9']

    def run(self):
        self.set_corner_cubestring(self.cube_state)
        self.set_edge_cubestring(self.cube_state)
        self.convert_dict_to_string()

    def set_corner_cubestring(self, cube_state):
        co = cube_state.co
        cp = cube_state.cp
        for i in range(len(co)):
            if co[i] == 0:
                key1, key2, key3 = self.cube_string_corner[i]
            elif co[i] == 1:
                key3, key1, key2 = self.cube_string_corner[i]
            else:
                key2, key3, key1 = self.cube_string_corner[i]
            corner_place = self.corner_place[cp[i]]
            self.cube_string_dict[key1] = corner_place[0]
            self.cube_string_dict[key2] = corner_place[1]
            self.cube_string_dict[key3] = corner_place[2]

    def set_edge_cubestring(self, cube_state):
        eo = cube_state.eo
        ep = cube_state.ep
        for i in range(len(eo)):
            if eo[i] == 0:
                key1, key2 = self.cube_string_edge[i]
            else:
                key2, key1 = self.cube_string_edge[i]
            edge_place = self.edge_place[ep[i]]
            self.cube_string_dict[key1] = edge_place[0]
            self.cube_string_dict[key2] = edge_place[1]

    def convert_dict_to_string(self):
        for key in self.primary_list:
            self.cube_string += self.cube_string_dict[key]





