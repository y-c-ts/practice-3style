# coding: UTF-8
from kociemba import solve
import numpy as np
import itertools
CORNER_CLOCK_WISE = 0
CORNER_ANTI_CLOCK_WISE = 1


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


class AlgState:
    def __init__(self, edge_buffer, corner_buffer, state):
        self.edge_normal = ['BL', 'BR', 'FR', 'FL', 'UB', 'UR', 'UF', 'UL', 'DB', 'DR', 'DF', 'DL']
        self.edge_inv = ['LB', 'RB', 'RF', 'LF', 'BU', 'RU', 'FU', 'LU', 'BD', 'RD', 'FD', 'LD']
        self.corner1 = ['ULB', 'UBR', 'URF', 'UFL', 'DBL', 'DRB', 'DFR', 'DLF']
        self.corner2 = ['LBU', 'BRU', 'RFU', 'FLU', 'BLD', 'RBD', 'FRD', 'LFD']
        self.corner3 = ['BUL', 'RUB', 'FUR', 'LUF', 'LDB', 'BDR', 'RDF', 'DLF']
        self.default_ep = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], dtype='int8')
        self.default_eo = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype='int8')
        self.default_co = np.array([0, 0, 0, 0, 0, 0, 0, 0], dtype='int8')
        self.default_cp = np.array([0, 1, 2, 3, 4, 5, 6, 7], dtype='int8')
        self.edge_target_cnd = []
        self.corner_target_cnd = []
        self.edge_buffer = edge_buffer
        self.corner_buffer = corner_buffer
        self.state_class = state
        self.edge_state_dict = {}
        self.corner_state_dict = {}
        self.define_all_edge_alg_state()
        self.define_all_corner_alg_state()

    def _get_edge_ind(self, string):
        arr1 = np.array(self.edge_normal)
        arr2 = np.array(self.edge_inv)
        res1 = np.where(arr1 == string)[0]
        res2 = np.where(arr2 == string)[0]
        if len(res1) > 0:
            idx = res1[0]
        else:
            idx = res2[0]
        return idx
    
    def _get_corner_ind(self, string):
        arr1 = np.array(self.corner1)
        arr2 = np.array(self.corner2)
        arr3 = np.array(self.corner3)
        res1 = np.where(arr1 == string)[0]
        res2 = np.where(arr2 == string)[0]
        res3 = np.where(arr3 == string)[0]
        if len(res1) > 0:
            idx = res1[0]
        elif len(res2) > 0:
            idx = res2[0]
        else:
            idx = res3[0]
        return idx

    def _get_co_place(self, target):
        if target in self.corner1:
            co = 0
        elif target in self.corner2:
            co = 1
        else:
            co = 2
        return co
        
    def define_ep_state(self, target1, target2):
        idx1 = self._get_edge_ind(target1)
        idx2 = self._get_edge_ind(target2)
        buffer_idx = self._get_edge_ind(self.edge_buffer)
        ep = self.default_ep.copy()
        ep[buffer_idx] = idx1
        ep[idx1] = idx2
        ep[idx2] = buffer_idx
        return ep

    def define_eo_state(self, target1, target2):
        buffer_idx = self._get_edge_ind(self.edge_buffer)
        idx1 = self._get_edge_ind(target1)
        idx2 = self._get_edge_ind(target2)
        eo = self.default_eo.copy()
        if target1 in self.edge_inv:
            eo[buffer_idx] = 1
        if (target2 in self.edge_inv) and (target1 in self.edge_normal):
            eo[idx1] = 1
        elif (target2 in self.edge_normal) and (target1 in self.edge_inv):
            eo[idx1] = 1
        if target2 in self.edge_inv:
            eo[idx2] = 1
        return eo

    def define_co_state(self, target1, target2):
        buffer_idx = self._get_corner_ind(self.corner_buffer)
        idx1 = self._get_corner_ind(target1)
        idx2 = self._get_corner_ind(target2)
        co = self.default_co.copy()
        co1 = self._get_co_place(target1)
        co2 = self._get_co_place(target2)
        if co1 == CORNER_CLOCK_WISE:
            co[buffer_idx] = 0
        elif co1 == CORNER_ANTI_CLOCK_WISE:
            co[buffer_idx] = 2
        else:
            co[buffer_idx] = 1
        if co2 == CORNER_CLOCK_WISE:
            co[idx1] = co1
        elif co2 == CORNER_ANTI_CLOCK_WISE:
            co[idx1] = (co1 + 2) % 3
        else:
            co[idx1] = (co1 + 1) % 3
        if co2 == CORNER_CLOCK_WISE:
            co[idx2] = 0
        elif co2 == CORNER_ANTI_CLOCK_WISE:
            co[idx2] = 1
        else:
            co[idx2] = 2
        return co
    
    def define_cp_state(self, target1, target2):
        idx1 = self._get_corner_ind(target1)
        idx2 = self._get_corner_ind(target2)
        buffer_idx = self._get_corner_ind(self.corner_buffer)
        cp = self.default_cp.copy()
        cp[buffer_idx] = idx1
        cp[idx1] = idx2
        cp[idx2] = buffer_idx
        return cp

    def make_edge_alg_state(self, e_target1, e_target2):
        eo = self.define_eo_state(e_target1, e_target2)
        ep = self.define_ep_state(e_target1, e_target2)
        state = self.state_class(self.default_cp, self.default_co, ep, eo)
        return state
    
    def make_corner_alg_state(self, c_target1, c_target2):
        co = self.define_co_state(c_target1, c_target2)
        cp = self.define_cp_state(c_target1, c_target2)
        state = self.state_class(cp, co, self.default_ep, self.default_eo)
        return state
    
    def define_all_corner_alg_state(self):
        corners = self.corner1 + self.corner2 + self.corner3
        corner_buffer = self.corner_buffer
        if len(corner_buffer) != 3:
            raise('コーナーbufferの指定が不正です。')
        print(corner_buffer)
        corners.remove(corner_buffer)
        corners.remove(corner_buffer[2] + corner_buffer[0] + corner_buffer[1])
        corners.remove(corner_buffer[1] + corner_buffer[2] + corner_buffer[0])
        for target1, target2 in itertools.permutations(corners, 2):
            target1_strings = np.array([i for i in target1])
            target2_strings = np.array([i for i in target2])
            if np.in1d(target1_strings, target2_strings).sum() != 3:
                key = target1 + '-' + target2
                self.corner_target_cnd.append(key)
                self.corner_state_dict[key] = self.make_corner_alg_state(target1, target2)
                 
    def define_all_edge_alg_state(self):
        edges = self.edge_normal + self.edge_inv
        edges.remove(self.edge_buffer)
        edges.remove(self.edge_buffer[::-1])
        for target1, target2 in itertools.permutations(edges, 2):
            if target1 != target2[::-1]:
                key = target1 + '-' + target2
                self.edge_target_cnd.append(key)
                self.edge_state_dict[key] = self.make_edge_alg_state(target1, target2)

    def get_multi_edge_alg_state(self, targets):
        for i, target in enumerate(targets):
            target = target.split('-')[1] + '-' + target.split('-')[0]
            if i == 0:
                state = self.edge_state_dict[target]
            else:
                tmp_state = self.edge_state_dict[target]
                state = state.apply_move(tmp_state)
        return state
    
    def get_multi_corner_alg_state(self, targets):
        for i, target in enumerate(targets):
            target = target.split('-')[1] + '-' + target.split('-')[0]
            if i == 0:
                state = self.corner_state_dict[target]
            else:
                tmp_state = self.corner_state_dict[target]
                state = state.apply_move(tmp_state)
        return state


class CubeString:
    def __init__(self, cube_state):
        self.cube_string = ''
        self.scramble = ''
        self.cube_string_dict = {'U5': 'U', 'F5': 'F', 'R5': 'R', 'L5': 'L', 'D5': 'D', 'B5': 'B'}
        self.cube_state = cube_state
        self.edge_place = ['BL', 'BR', 'FR', 'FL', 'UB', 'UR', 'UF', 'UL', 'DB', 'DR', 'DF', 'DL']
        self.corner_place = ['ULB', 'UBR', 'URF', 'UFL', 'DBL', 'DRB', 'DFR', 'DLF']
        self.cube_string_edge = [('B6', 'L4'), ('B4', 'R6'), ('F6', 'R4'), ('F4', 'L6'), ('U2', 'B2'), ('U6', 'R2'),
                                 ('U8', 'F2'), ('U4', 'L2'), ('D8', 'B8'), ('D6', 'R8'), ('D2', 'F8'), ('D4', 'L8')]
        self.cube_string_corner = [('U1', 'L1', 'B3'), ('U3', 'B1', 'R3'), ('U9', 'R1', 'F3'), ('U7', 'F1', 'L3'),
                                   ('D7', 'B9', 'L7'), ('D9', 'R9', 'B7'), ('D3', 'F9', 'R7'), ('D1', 'L9', 'F7')]
        self.primary_list = ['U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8', 'U9', 'R1', 'R2', 'R3', 'R4',
                             'R5', 'R6', 'R7', 'R8', 'R9', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8',
                             'F9', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'L1', 'L2', 'L3',
                             'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7',
                             'B8', 'B9']
        self.run()

    def run(self):
        self.set_corner_cubestring(self.cube_state)
        self.set_edge_cubestring(self.cube_state)
        self.convert_dict_to_string()
        self.scramble = solve(self.cube_string)

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
