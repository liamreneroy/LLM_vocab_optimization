# LLM_vocabulary
Generating expressive robot vocabulary sets via proxy-based optimization.

### Link to Research Paper
TBD

## Main Files and User Study
This codebase uses the framework as described in our submitted paper. In this implimentation, the GPT-4o model is used. The main files in this repo are:




### Jupyter Notebook used to Generate the Accuracy Arrays and run the Optimization Hill-Climb: 
Notebook includes explanations of the OpenAI API hyper-parameters used in this task, along with values.
https://github.com/liamreneroy/LLM_vocab_optimization/blob/main/scripts/main.ipynb


### Pseudo-Code for the Optimization Hill-Climb Algorithm and Sub-Methods: 
Sub methods include distance calculation, objecive function scoring method, initialization method.
https://github.com/liamreneroy/LLM_vocab_optimization/tree/main/media/algorithm_pseudocode


### Jupyter Notebook used to Validate the Accuracy Proxy Using the Test Dataset
Notebook includes explanations of the OpenAI API hyper-parameters used in this task, along with values.
https://github.com/liamreneroy/LLM_vocab_optimization/blob/main/scripts/proxy_validation.ipynb


### Prompt Format Used for the Accuracy Proxy. Includes Sample Response.
https://github.com/liamreneroy/LLM_vocab_optimization/blob/main/media/accuracy_proxy/acc_proxcy_prompt_reply.txt


### Outputs of the Main Optimization Hill-Climb Algorithm with Weight Analysis
https://github.com/liamreneroy/LLM_vocab_optimization/blob/main/media/optimization/main_output_with_weight_analysis.txt


### Excel File Containing Motions Selected from the Optimization Function
https://github.com/liamreneroy/LLM_vocab_optimization/tree/main/data/study_results


### Excel File Containing Raw and Organized Results of the User Study
https://github.com/liamreneroy/LLM_vocab_optimization/tree/main/data/study_results


### All Confusion Matrices Plots
https://github.com/liamreneroy/LLM_vocab_optimization/tree/main/plots/conf_matrix


### Statistical Analyses Implimented in R
https://github.com/liamreneroy/LLM_vocab_optimization/tree/main/stats



## Packages to Install:
pygame   (see this webpage ~ https://www.pygame.org/wiki/GettingStarted)  
jupyterlab, numpy, termcolor, openpyxl, nbconvert-webpdf, openai, wandb  


Either use:    
--> sudo apt-get install <package_name>  
--> python3 -m pip install <package_name>  
--> conda install -c conda-forge <package_name>  


Example using conda:  
--> conda install -c conda-forge <package_name>  

jupyterlab or notebook  
numpy  
termcolor  
openpyxl  
nbconvert-webpdf              
openai
wandb  


## Owner: 
Liam Rene Roy
Liamreneroy@gmail.com
Liam.roy@monash.edu