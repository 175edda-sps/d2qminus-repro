# Reinforcement Learning Experiments

## 1. Train RL model
First step is to train a Doc2Query model that optimizes the ELECTRA score directly using reinforcement  learning.  To do, just run this script
```
python experiments/rl/trl_ppo_d2q.py
```
### 2. Generate the expansion queries 
Choose the model at the target checkpoint, then employ the model to generate the expansion queries using the generation script from [DocT5Query](https://github.com/castorini/docTTTTTquery) repo.