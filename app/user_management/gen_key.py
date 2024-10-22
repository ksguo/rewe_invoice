import secrets

# gen random 256 secret key
secret_key = secrets.token_hex(32)
print(f"Your secret key is: {secret_key}")
"""
run this py one time and get the secret key ,then put in .env file
SECRET_KEY=your SECRET_KEY which generate by gen_key.py
"""
