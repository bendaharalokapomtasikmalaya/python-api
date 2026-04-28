from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET")

class Guest(BaseModel):
    name: str
    message: str

@app.get("/")
def root():
    return {"status": "Python API OK"}

@app.get("/guestbook")
def get_guestbook():
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    res = requests.get(f"{SUPABASE_URL}/rest/v1/guestbook?select=*&order=created_at.desc", headers=headers)
    return res.json()

@app.post("/guestbook")
def create_guest(guest: Guest):
    if not guest.name or not guest.message:
        raise HTTPException(status_code=400, detail="Nama & pesan wajib")

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    payload = {
        "name": guest.name,
        "message": guest.message
    }

    res = requests.post(f"{SUPABASE_URL}/rest/v1/guestbook", json=payload, headers=headers)

    if res.status_code not in (200, 201):
        raise HTTPException(status_code=500, detail=res.text)

    return {"status": "ok"}
