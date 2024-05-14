# Local-Crime-Analysis
## About

## Installation & Setup
1. Clone the repository to your local machine.
2. Change to the outer 'mysite' directory.
   ```
   cd mysite
   ```
3. Create a virtual environment and install from the requirements file.
   ```
   python3 -m venv venv
   source ./venv/bin/activate
   pip3 install -r requirements.txt
   ```
4. Run the server on your local machine.
   ```
   python3 manage.py runserver
   ```
  After running this command, there will be a url in the terminal where you can access the locally-hosted website (http://127.0.0.1:8000/).


## Endpoints
| Endpoint              | Request | Description | Example |
| :---------------- | :------: | ----: | ----: |
| /crimes/`<postcode>`  |   GET   | A page with stats/visualisations about<br>crimes around the given postcode | http://127.0.0.1:8000/crimes/N1C4AX/ |
