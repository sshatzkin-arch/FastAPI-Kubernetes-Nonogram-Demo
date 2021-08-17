import numpy as np
from fastapi import FastAPI
from nonogram import Nonogram
from database import connect, print_nonos, get_nonos, push_nono, get_nonos_by
import logging

app = FastAPI()

@app.get("/")
async def root():
  conn = connect()
  nonograms = get_nonos(conn)
  return {"nonograms": nonograms}

@app.get("/by/")
async def get_by(id: int = None, name: str = None, min_width: int = 0, max_width: int = 10000, min_height: int = 0, max_height: int = 10000):
  print("Starting Connection")
  conn = connect()
  nonograms, query = get_nonos_by(conn, ID = id, name = name, min_width = min_width, max_width = max_width, min_height = min_height, max_height = max_height)
  return {"query": query, "nonograms": nonograms}


@app.get("/nonogram/{rows}/{cols}/")
async def get_nono(rows: int, cols: int):
  test_puzz = Nonogram(rows, cols)
  print(test_puzz.solution)
  print(test_puzz.encode("Test Puzz"))
  return {"clues": test_puzz.clues, "solution": test_puzz.solution.tolist()}
    
# Generates a random puzzle and pushes it to SQL
@app.get("/nonogram/{rows}/{cols}/push")
async def get_nono_push(rows: int, cols: int):
  conn = connect()
  test_puzz = Nonogram(rows, cols)
  print(test_puzz.solution)
  name = f"Test {str(rows)}x{str(cols)} Puzzle"
  print(name)
  push_nono(conn, test_puzz.encode(name))
  return {"clues": test_puzz.clues, "solution": test_puzz.solution.tolist()}