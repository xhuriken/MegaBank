from fastapi import FastAPI, Depends, HTTPException
from .state import *

def get_acc(iban: str):
    acc = accounts.get(iban)
    if not acc:
        raise HTTPException(404, "Iban not found")
    return acc

