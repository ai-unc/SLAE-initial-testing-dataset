# Parsing .mdl Files

There is a python script to parse the .mdl files into .json files, one for general use and the other for Kumu.

## Usage
Place the .mdl file to be parsed in the models subdirectory. Use the following command to then parse that file:
```py
python parser.py -model="model_file_name"
```

#### Example
```py
python parser.py
-model="model.mdl"
```

The output of the parser will be saved to the json and kumu subdirectories.

You can use the following commands for usage help:
```py
python parser.py -h
python parser.py --help
``` 