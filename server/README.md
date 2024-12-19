# FOMO Server


1. Create a python virtual environment
```
> python3 -m venv venv
```

2. Activate the virtual environment
```
> source venv/bin/activate
```
3. Install required packages
```
> python3 -m pip install -r requirements.txt
```
4. Create a `.env` file with the following [values from Supabase](https://supabase.com/docs/guides/api#api-url-and-keys)
```
SUPABASE_URL=...
SUPABASE_KEY=...
```

5. Run a local server
```
> uvicorn main:app --reload
```

> If you added new python packages that are require to run the scripts, please run `pip freeze > requirements.txt` before pushing the changes.
