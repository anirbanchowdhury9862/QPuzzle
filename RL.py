import json, copy
import numpy as np

BEGINNING_STATE=np.array([
                    [0,1,2],
                    [3,4,5],
                    [6,7,8]
                ])
actions = {
    0: {'type': 'top',  'movement': (-1, 0)},    
    1: {'type': 'down', 'movement': ( 1, 0)},    
    2: {'type': 'right','movement': ( 0,-1)},  
    3: {'type': 'left', 'movement': ( 0, 1)}     
}

class QModel:
    def __init__(self,model_path):
        weights,policy=model_path+'/weights.json',model_path+'/policy.json'
        self.weights=json.load(open(weights))
        self.weights={key:list(map(float,self.weights[key][1:-1].split(',')))  for key in self.weights}
        self.policy=json.load(open(policy))
        self.policy={key:list(map(int,self.policy[key]))  for key in self.policy}
    def predict(self,state,policy_only=False):
        if type(state)==type(np.array([])):
            state_key=''.join(map(str,state.flatten()))
        if state_key in self.policy:return self.policy[state_key]
        elif not policy_only:
            actions=self.weights.get(state_key)
            if actions:return [np.argmax(actions)]
            else:return None
        else:return None
    def __call__(self,state,policy_only=False):
        return self.predict(state,policy_only)

def generate_random_state(initial_state=BEGINNING_STATE):
    state=copy.deepcopy(initial_state)
    pos = {'row': 2, 'col': 2}
    # step_range=np.random.randint(40,200)
    for i in range(40):
        step=np.random.randint(4)
        pos_row=pos['row']+actions[step]['movement'][0]
        pos_col=pos['col']+actions[step]['movement'][1]
        if 0<=pos_row<=2 and 0<=pos_col<=2:
            state[pos_row][pos_col],state[pos['row']][pos['col']]=state[pos['row']][pos['col']],state[pos_row][pos_col]
            pos['row']=pos_row
            pos['col']=pos_col
            
    return state,pos

def reward_fn(state,initial_state):
    # return np.array_equal(state, initial_state)
    # return 2*np.sum(state==initial_state)-9
    return -np.sum(abs(state-initial_state))

def take_action(state, pos, action):
    pos_row = pos['row'] + actions[action]['movement'][0]
    pos_col = pos['col'] + actions[action]['movement'][1]
    new_state = copy.deepcopy(state)
    if 0 <= pos_row <= 2 and 0 <= pos_col <= 2:
        new_state[pos_row, pos_col], new_state[pos['row'], pos['col']] = new_state[pos['row'], pos['col']], new_state[pos_row, pos_col]
        pos['row'], pos['col'] = pos_row, pos_col
    return new_state, pos

if __name__=='__main__':
    # model=QModel(weights='../weights.json',policy='../policy.json')
    model=QModel('models/model_1')
    state,pos=generate_random_state()
    soln=model(state)
    initial_reward=reward_fn(state,BEGINNING_STATE)
    print(f'soln {soln} initial reward {initial_reward}')
    
