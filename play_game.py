from RL import QModel, generate_random_state, BEGINNING_STATE, reward_fn, take_action
import random
import numpy as np
import argparse
from render_puzzle import GameRenderer

def solve_puzzle():
    state,pos = generate_random_state()
    
    steps = 0
    done=0
    while reward_fn(state,BEGINNING_STATE):
        if steps>=300:
            actions=x_model(state,policy_only=True)    
        else:
            actions=x_model(state)
        if not actions:actions=[np.random.randint(4)]   
        for action in actions:
            state, pos = take_action(state, pos, action)
            steps+=1     
            
                
    if reward_fn(state,BEGINNING_STATE)==0:
        done=1
        # print(steps)
        # print(state)
        

    return steps,done

def test_model(ngames):
    avg_steps = 0
    games_won=0
    for _ in range(ngames):
        steps,done= solve_puzzle()
        if done:
            games_won+=1
            avg_steps+=steps

    avg_steps /= games_won
    print(f'avg game steps {avg_steps} for {games_won} games')



if __name__=='__main__':
    parser = argparse.ArgumentParser(description="AI vs Human to solve sliding puzzle")
    parser.add_argument('--test_mode', type=bool, help='Set True to see avg steps the model takes to win games', required=not True,default=False)
    parser.add_argument('--games',type=int, help='Number of games to play, only works when TEST_MODE is set to True', required=not True)
    parser.add_argument('--model',type=str, help='Model path', required=not True)
    parser.add_argument('--render',type=bool, help='ORIGINAL GUI GAME', required=not True,default=True)
    parser.add_argument('--image',type=str, help='ORIGINAL GUI GAME', required=not True,default=None)
    

    args = parser.parse_args()
    test_mode = args.test_mode
    model_path=args.model
    render=args.render
    image=args.image
    x_model=QModel(model_path)
    if test_mode:
        render=False
        ngames=args.games
        if not ngames:
            print('specify number of games')
        test_model(args.games)
    elif render:
        renderer=GameRenderer()
        renderer.render_game(x_model,image)




