import streamlit as st
import width
import ResolutionModel as resolve
import Clause
import Literal


hasStarted = False
hasFinished = False

if not hasStarted:

    input = st.text_input("Enter clauses in the format {A,B},{~A,C},{~B,~C,D}", value="{A,B},{~A,C},{~B,~C,D}")
    tryStart = st.button("Submit")


    model = resolve.ResolutionModel.parse(input)

    if model.num_clauses() > 0:
        hasStarted = True

if hasStarted:
    clauses = model.get_clauses()

    grid = []

    width = width.width(len(clauses))

    for i in range(width):
        grid.append(st.columns(width))

    if 'has_clause' not in st.session_state:
        st.session_state.has_clause = False
    
    if 'first_clause' not in st.session_state:
        st.session_state.first_clause = None

    # TODO add has started, has finished to session states, add states for initializing vs. carrying on model

    def click_button(clause: Clause.Clause):
        if st.session_state.has_clause:
            clauses.append(Clause.Clause.resolve(st.session_state.first_clause, clause, Literal.Literal(False, "A")))
            st.session_state.has_clause = False
        else:    
            st.session_state.has_clause = True
            st.session_state.first_clause = clause

    st.session_state
    clauses

    element = 0
    row = 0
    col = 0
    diagonal = 0

    for diagonal in range(2*width):
        row = diagonal if diagonal < width else width - 1
        col = 0 if diagonal < width else diagonal - width + 1
        while row >= 0 and col < width:
            if (((row%2)==0 and (col%2)==0) or ((row%2)!=0 and (col%2)!=0)) and element < len(clauses):
                grid[row][col].button(f"{clauses[element]}", key=f"button_{element}", on_click=click_button, args=[clauses[element]])
                element += 1
            row -= 1
            col += 1


