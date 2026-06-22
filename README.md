# README

This project can calculate the Spearman's rank correlation coefficient and create scatterplots which show the correlation (or lack thereof) between the modernity and code quality for Python projects. It uses Vermin and PyLint in order to get the modenrity features and the code quality. 

## FEATURES
The codebase contains the following files which have the following features:

What to download before running any files:
    - Download Vermin: pip install vermin
    - Download PyLint: pip install pylint


To make a global graph which shows a dot per repotisory follow these steps:
1. Run verminPerFeature.py on the directiroy where all of the repositories can be found. 
    change repos_path to another directory if you wish so. Depending on the amount of
    repositories, this might take a few hours.
2. Run pylintStatsSummary.py or pylintPerMessage.py in order to receive the information
    from PyLint. pylintStatSummary.py may run faster but retreives no information to make the 
    graphs for a single repository while pylinyPerMessage.py will do this. This could safe
    time if you plan on making both graphs. Both will take a few days to run depending on 
    the size of the data and your environment. Ps: in the meantime, you can use VSCodeCounter
    or another tool to get the lines of code for the projects. The lines of code for the current
    projects is already in the directory loc_dict in the plotter files.
3. Run pylintStatsPerFile if you chose to run pylintPerMessage.py on the output of step 2.
4. Run verminToStats.py on the output of step 1.
5. Lastly, you can run plotterAllRepos.py to create the graphs and get the Spearman's rank
    correlation coefficient. 

To create the Mahalanobis plot follow these steps:
1. Plot the global graph using the steps discribed above.
2. Use the x and y in the code (print them and copy past them into the 
    plotterMahalanobisDistance.py or alter the code so it is done automatically).
3. Run plotterMehalanobisDistance.py.

To make a graph for one repository follow these steps:
1. If you have not done this yet: run pylintPerMessage.py on the repository by changing 
    the repo_root to the path of the directory that the repository or multiple repositories 
    are in (the repository or repositories one you want a graph of). This will take some time depending on the size of the repository.
    Optional: you can change the output_root to something you prefer over the already 
    given output_root.
2. Run linesOfCodePerFile.py on the repository. Change file_name, repo_path and mkfile if needed.
3. Run pylintStatsPerFile.py on the output of step 1 and step 2, so change repo_name, file_name and 
    loc_file accordingly
4. Lastly, run plotterOneRepo.py to plot the repository and get the Spearman's rank 
    correlation coefiicient. This will return the Pearson correlation as well as the graph. 
    You can change the colour of the dots by changing "color_dots".

The .pylintrc file contains the configurations for PyLint. In this file, some messages have been 