import numpy as np
import copy
import json
from RL import take_action, reward_fn, BEGINNING_STATE, actions
import argparse
import time
import os
def save_model(Q,policy,new_model_path):
    Q_x={key:str(Q[key]) for key in Q}
    print(len(policy),len(Q_x))

    with open(f'{new_model_path}/policy.json','w') as output:
        json.dump(policy,output)
    with open(f'{new_model_path}/weights.json','w') as output:
        json.dump(Q_x,output)


def generate_random_state():
    state=copy.deepcopy(BEGINNING_STATE)
    pos = {'row': 2, 'col': 2}
    # step_range=np.random.randint(40,200)
    for i in range(10000):
        step=np.random.randint(4)
        state_key=''.join(map(str,state.flatten()))
        if state_key not in policy:
            return state,pos
        pos_row=pos['row']+actions[step]['movement'][0]
        pos_col=pos['col']+actions[step]['movement'][1]
        if 0<=pos_row<=2 and 0<=pos_col<=2:
            state[pos_row][pos_col],state[pos['row']][pos['col']]=state[pos['row']][pos['col']],state[pos_row][pos_col]
            # print(state)
            # print('\n')
            pos['row']=pos_row
            pos['col']=pos_col
            
    return state,pos
if __name__=='__main__': 

    parser = argparse.ArgumentParser(description="Train the Q learning model to solve the puzzle")
    parser.add_argument('--transfer_learning',action='store_true', help='If set to False will train a fresh model else will do Transfer learning. \
                        Specify pretrained model path in case of transfer learning.', required=not True)
    parser.add_argument('--pretrained_model', type=str, help='Path for pretrained model to load for Transfer learning.\
                         RESET flag should be False.',required=not True,default=None)
    args = parser.parse_args()
   

    new_stamp=time.ctime()
    if not os.path.exists(os.path.join('models')):
        os.mkdir('models')
    new_model_path='models/model-'+new_stamp
    pretrained_path=args.pretrained_model
    os.mkdir(new_model_path)
    if not args.transfer_learning:
        Q = {}
        policy={}
        epsilon=1
    else:
        epsilon=0.2
        Q_f,policy_f=open(f'{pretrained_path}/weights.json'),open(f'{pretrained_path}/policy.json')
        Q,policy=json.load(Q_f),json.load(policy_f)
        Q={key:list(map(float,Q[key][1:-1].split(',')))  for key in Q}
    
    gamma = 0.9  
    alpha = 0.05
    
    

    num_episodes = 20000000
    epsilon_decay=0.001

    for episode in range(num_episodes):
        
        state,pos = generate_random_state()
        done=False
        steps=0
        start_state=copy.deepcopy(state)
        path=''
        # start_state_key=tuple(start_state.flatten())
        start_state_key=''.join(map(str,start_state.flatten()))
        # if start_state_key in policy:continue
        while not done and steps<=20:
            # state_key=tuple(state.flatten())
            state_key=''.join(map(str,state.flatten()))
            
            if state_key not in Q:Q[state_key]=[0.,0.,0.,0.];
            if np.random.rand() < epsilon:
                action = np.random.randint(4)  
            else:
                action=np.argmax(Q[state_key])
            
            next_state, next_pos = take_action(state, pos, action)

            # next_state_key=tuple(next_state.flatten())
            next_state_key=''.join(map(str,next_state.flatten()))
            
            if state_key!=next_state_key:
                path+=str(action)
            reward = reward_fn(next_state,BEGINNING_STATE) 
            if next_state_key not in Q:
                Q[next_state_key]=[0.,0.,0.,0.]
            
            next_max = np.max(Q[next_state_key])
        
            
            
        
            Q[state_key][action] = (1 - alpha) * Q[state_key][action] + alpha * (reward + gamma * next_max)
            state, pos = next_state, next_pos
            steps+=1
            if reward_fn(state,BEGINNING_STATE)==0:
                if epsilon<0:epsilon=0.2
                if start_state_key not in policy or len(path)<len(policy[start_state_key]):
                    policy[start_state_key]=path
                    epsilon=epsilon-epsilon_decay
                done=True
                #  epsilon=epsilon-epsilon_decay
                break
        if done:
            print(f'episode {episode } converged in {steps} steps; epsilon {epsilon} ;policy {len(policy.keys())}; total states {len(Q.keys())}')
            
        if episode%10000==0:
            save_model(Q,policy,new_model_path) 
    


