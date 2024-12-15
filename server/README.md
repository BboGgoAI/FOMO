# Scripts

## How to run scripts to collect events data from external sources


1. Create a python virtual environment
```
> python3 -m venv venv

```

2. Activate the virtual environmetn
```
> source venv/bin/activate

```
3. Install required packages
```
> python3 -m pip install -r requirements.txt
```
4. Run the script (e.g., eventbrite.py)
```
> python3 main.py
```

> If you added new python packages that are require to run the scripts, please run `pip freeze > requirements.txt` before pushing the changes.

'uvicorn main:app --reload'

