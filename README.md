# <font color='red' size=6><b> QPuzzle </font> <br>
## <font color='green' size=5><b>A Reinforcement learning agent trained with Q learning algorithm to solve any sliding puzzle created from any image. The model takes the grid as input and predicts the next best action to win the game. Desigining proper reward functions ensure success of reinforcement learning models.</font>
```
$ python play_game.py --help
usage: play_game.py [-h] [--test_mode TEST_MODE] [--games GAMES] [--model MODEL] [--render RENDER] [--image IMAGE]

AI vs Human to solve sliding puzzle

options:
  -h, --help            show this help message and exit
  --test_mode TEST_MODE
                        Set True to see avg steps the model takes to win games
  --games GAMES         Number of games to play, only works when TEST_MODE is set to True
  --model MODEL         Model path
  --render RENDER       ORIGINAL GUI GAME
  --image IMAGE         Image for the sliding puzzle
```
## For testing a model for avg steps it takes to win games
```
$ python play_game.py --test_mode True --model models/model_2 --games 500
avg game steps 12.104 for 500 games
```
## For solving the sliding puzzle
```
$ python play_game.py --model models/model_2 --image terminator.png 
```


https://github.com/anirbanchowdhury9862/QPuzzle/assets/20869692/59d6bb8e-33ac-484e-83fe-75d3727854db

## For training the Q model
```
$ python train_model.py --help
usage: train_model.py [-h] [--transfer_learning] [--pretrained_model PRETRAINED_MODEL]

Train the Q learning model to solve the puzzle

options:
  -h, --help            show this help message and exit
  --transfer_learning   If not used will train a fresh model else will do Transfer learning. Specify pretrained model path in case    
                        of transfer learning.
  --pretrained_model PRETRAINED_MODEL
                        Path for pretrained model to load for Transfer learning.
```




