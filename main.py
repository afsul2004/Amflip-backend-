import mysql.connector
from fastapi import HTTPException, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from  pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class log(BaseModel):
    name: str = ""
    email: str
    password: str

# a = mysql.connector.connect( host="localhost", user="root", passwd="", database="ecomproff")
import os
import mysql.connector

a = mysql.connector.connect(
    host=os.environ.get("localhost"),
    user=os.environ.get("root"),
    password=os.environ.get(""),
    database=os.environ.get("ecomproff"),
    port=int(os.environ.get(3306))
)


@app.post("/register")
def register(l : log):
    cursor = a.cursor()
    check_query = """SELECT email FROM login1 WHERE email = %s"""
    cursor.execute(check_query, (l.email,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.close()
        return ["Email already exists"]
    cursor.execute(f"insert into login1 (name, email, password) values ('{l.name}','{l.email}', '{l.password}')")
    a.commit()
    cursor.close()
    return ["Registration Successful"]

@app.post("/login")
def login(l: log):
    cursor = a.cursor()
    query = """SELECT * FROM login1 WHERE email = %s AND password = %s """
    cursor.execute(query, (l.email, l.password))
    data = cursor.fetchone()
    cursor.close()
    if data:
        return {
            "message": "Login Successful",
            "username": data[1]
        }
    return ["Invalid ID or Password"]

@app.post("/forgot-password")
def forgot_password(l : log):
    cursor = a.cursor()
    cursor.execute("SELECT * FROM login1 WHERE email = %s", (l.email,))
    user = cursor.fetchone()
    if not user:
        cursor.close()
        return {
            "message": "Email not found"
        }
    cursor.execute("UPDATE login1 SET password = %s WHERE email = %s", (l.password, l.email))
    a.commit()
    cursor.close()
    return {
        "message": "Password updated successfully"
    }
