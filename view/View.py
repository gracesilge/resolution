import streamlit as st
import width
from Resolution import ResolutionModel as resolve


hasStarted = False

if not hasStarted:

    input = st.text_input("Enter clauses in the format {A,B},{~A,C},{~B,~C,D}", value="{A,B},{~A,C},{~B,~C,D}")
    tryStart = st.button("Submit")


    model = resolve.parse("{A,B},{~A,C},{~B,~C,D},{~D,E},{~E},{F,~G},{G}")

    if model.num_clauses() > 0:
        hasStarted = True

if hasStarted:
    list = model.get_clauses()

    grid = []

    width = width.width(len(list))

    for i in range(width):
        grid.append(st.columns(width))

    element = 0
    row = 0
    col = 0
    diagonal = 0

    for diagonal in range(2*width):
        row = diagonal if diagonal < width else width - 1
        col = 0 if diagonal < width else diagonal - width + 1
        while row >= 0 and col < width:
            if (((row%2)==0 and (col%2)==0) or ((row%2)!=0 and (col%2)!=0)) and element < len(list):
                grid[row][col].button(f"Button {list[element]}", key=f"button_{element}")
                element += 1
            row -= 1
            col += 1