# rewe-invoice



## Features
* [X] Ready-to-use register, login routes
* [X] Ready-to-use social OAuth2 login flow
* [X] Dependency callables to inject current user in route
* [X] Customizable database backend
    * [X] [SQLAlchemy ORM async](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html) included
* [X] Authentication backends
    * [X] Strategies: JWT
* [X] Full OpenAPI schema support, even with several authentication backends
* [X] Ready-to-use upload,delete,list file in route
* [X] Ready-to-use scan and extract invoice data in route
* [X] Ready-to-use analyze data with AI in route


## Development

### Setup environment
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
### Dependencies
```
brew install pytesseract
brew install tesseract-lang
brew install poppler
``` 


#### how to manual test router function
```
-Fastapi SwaggerUI
-Postman
```

### Format the code
```
venv/bin/flake8
```

### Run unit tests

You can run all the tests with:

```
venv/bin/pytest --cov -v
```
