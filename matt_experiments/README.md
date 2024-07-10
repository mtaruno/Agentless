
### codegeex-4 + agentless on SWE Bench lite

Matt tries to run codegeex-4 + agentless on SWE Bench lite. 

General repo: 
https://github.com/OpenAutoCoder/Agentless?tab=readme-ov-file

This is the guide I follow:
https://github.com/OpenAutoCoder/Agentless/blob/main/README_swebenchlite.md



### Localization 

On `utils/api_requests` I make a new config and engine for codegeex.

Download the `repo_structures` folder for swe-benchlite. Put it in the root directory. 

```
export PROJECT_FILE_LOC='repo_structures' 
```

I add these imports at `FL.py`  where appropriate and replace relevant chatgpt requests/engines with codegeex-4 ones. 
```
from agentless.util.api_requests import (
	create_codegeex_config,
	num_tokens_from_messages,
	request_codegeex_engine
)
```

Generate the edit locations: 
```
python agentless/fl/localize.py --file_level --related_level --fine_grain_line_level \
                                --output_folder results/location --top_n 3 \
                                --compress \
                                --context_window=10 \
                                --temperature 0.8 \
                                --num_samples 4
```

This will save all the localized locations in results/location/loc_outputs.jsonl with the logs saved in results/location/localize.log

Note that in the last stage of our localization we perform sampling (i.e., with --temperature 0.8 and --num_samples 4) to obtain 4 sets of edit locations.

Following the steps described in our paper, we then perform merging to form a bigger list of edit locations.

This probably is something that will improve performance: "We can further improve performance to 78 fixes by sampling the LLM multiple times and selecting a patch using majority voting"

Run the following command to merge:

```
python agentless/fl/localize.py --merge \
                                --output_folder results/location_merged \
                                --start_file results/location/loc_outputs.jsonl \
                                --num_samples 4
```

But I still got the resulting `loc_merged_0-0_outputs.jsonl`. 







### Repair 

```
python agentless/repair/repair.py --loc_file results/location/loc_outputs.jsonl \
                                  --output_folder results/repair \
                                  --loc_interval --top_n=3 --context_window=10 \
                                  --max_samples 10  --cot --diff_format \
                                  --gen_and_process 
```


It is able to run even though I am not really going through with the sampling so the performance might be worse... I'm not sure how much of an effect the sampling makes. 



Question:  What does the trying the n-th sample mean?  

After getting the files in the output, which is in results/repair, I probably need to repair to get the predictions that I can run on swe-bench-lite. 



```
python agentless/repair/rerank.py --patch_folder results/repair_run_1 --num_samples 42 --deduplicate --plausible
```

This command will produced the all_preds.jsonl that contains the final selected patch for each instance_id which you can then directly use your favorite way of testing SWE-bench for evaluation!




#### Greedy and Temperature Sampling



### Codegeex4 experiment

It seems that `num_samples` need to be increased for the localization steps to 4.

A little test using `agentless/util/codegeex4.py` to see if it works.



