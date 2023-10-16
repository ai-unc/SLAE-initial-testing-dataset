# SLAE Initial Testing Dataset

### Contains text & pdf files of initial papers used purely for testing and prototyping + corresponding json input files

## Adding a paper

There is a python script to quickly rename a paper file and create a corresponding json file

```py
python script.py -file="paper_file_name" -doi="paper_doi"  -title="paper_title"
```

Example:

```py
python script.py
-file="paper.txt"
-doi="10.1111/j.1460-9568.2012.08013.x"
-title="Orexin / hypocretin 1 receptor antagonist reduces heroin self-administration and cue-induced heroin seeking"
```

**You will need to manually add the variable relationships to the input json file**
