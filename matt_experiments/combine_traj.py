import pandas as pd 
# combine everything into one coherent trajectory


loc_outputs = pd.read_json("../gpt_results/loc_outputs.jsonl", lines=True)

bug_traj, all_traj = [], []


for bug in df.iterrows():
    create_traj(bug)    

def create_traj(bug):
    bug_traj.append({"role": "user", "content": bug['related_loc_traj']['prompt']})
    bug_traj.append({"role": "assistant", "content": bug['related_loc_traj']['response']})
    bug_traj.append({"role": "user", "content": bug['related_loc_traj']['prompt2']})
    



# Desired format: [{"role": "", "content": ""} , ]
