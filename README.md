# THIS IS LAB DIJANGO 2

## INSTALL ENVIROMENT 
### Step 1: Create vituel enviroment
```
python -m venv .venv
```
### Step 2: Activate enviroment
```
.venv/Scripts/activate (Windowns)
.venv/bin/activate (Ubuntu/MacOS)
```
### Step 3: Install packages/ libraries
```
pip install -r requirements.txt
```

## RUN SCRIPTS

### Generator Database
```
cd lab2
python seed.py
```

### Test Scripts 
```
python query_test.py
```


## Migration 
```
# cd lab2/blog/migrations # to tracking migration forward-backward
python manage.py showmigrations blog # Show migration
```