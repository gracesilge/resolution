import streamlit as st
import width
import ResolutionModel as resolve

if 'has_clause' not in st.session_state:
        st.session_state.has_clause = False
    
if 'first_clause' not in st.session_state:
    st.session_state.first_clause = None

if 'second_clause' not in st.session_state:
    st.session_state.second_clause = None

if 'current_state' not in st.session_state:
    st.session_state.current_state = 1

if 'model' not in st.session_state:
    st.session_state.model = None

if 'clauses' not in st.session_state:
    st.session_state.clauses = None

if st.session_state.current_state == 1:

    input = st.text_input("Enter clauses in the format {A,B} {~A,C} {~B,~C,D}")
    tryStart = st.button("Submit")


    if tryStart:
        try:
            st.session_state.model = resolve.ResolutionModel.parse(input)
            if st.session_state.model.num_clauses() > 0:
                st.session_state.current_state = 2
                st.rerun()
        except (ValueError) as e:
            st.error("Invalid format, try again.")
        
    
    

if st.session_state.current_state == 2:
    col1, col2 = st.columns([5, 1])
    with col2:
        reset = st.button("Reset", type="tertiary")
        if reset:
            st.session_state.current_state = 1
            st.session_state.has_clause = False
            st.session_state.first_clause = None
            st.session_state.second_clause = None
            st.session_state.model = None
            st.session_state.clauses = None
            st.rerun()

    with col1:
        if st.session_state.has_clause:
        # Display the two clauses being resolved
            clause1 = st.session_state.model.get_clauses()[st.session_state.first_clause]
            st.write(f"Resolving: {clause1} and ...")
        else:
            st.write("Resolving: ... and ...")

        st.session_state.clauses = st.session_state.model.get_clauses()

        grid = []

        width = width.width(len(st.session_state.clauses))

        for i in range(width):
            grid.append(st.columns(width))


        # TODO add has started, has finished to session states, add states for initializing vs. carrying on model

        def click_button(index: int):
            if st.session_state.has_clause:
                if (st.session_state.model.numResolveLiterals(st.session_state.first_clause, index) == 0):
                    st.warning("These clauses cannot be resolved on any literal-negation pair.")
                    st.session_state.first_clause = None
                    st.session_state.has_clause = False
                    return
                if (st.session_state.model.numResolveLiterals(st.session_state.first_clause, index) == 1):
                    st.session_state.model.resolve(st.session_state.first_clause, index, st.session_state.model.getEasyLiteral(st.session_state.first_clause, index))
                    st.session_state.clauses = st.session_state.model.get_clauses()
                    if any(len(c.get_literals()) == 0 for c in st.session_state.clauses):
                        st.session_state.current_state = 4
                else:
                    st.session_state.current_state = 3
                    st.session_state.second_clause = index
                st.session_state.has_clause = False
            else:    
                st.session_state.has_clause = True
                st.session_state.first_clause = index
        
        st.session_state.clauses = st.session_state.model.get_clauses()

        element = 0
        row = 0
        col = 0
        diagonal = 0

        for diagonal in range(2*width):
            row = diagonal if diagonal < width else width - 1
            col = 0 if diagonal < width else diagonal - width + 1
            while row >= 0 and col < width:
                if (((row%2)==0 and (col%2)==0) or ((row%2)!=0 and (col%2)!=0)) and element < len(st.session_state.clauses):
                    grid[row][col].button(f"{st.session_state.clauses[element]}", key=f"button_{element}", on_click=click_button, args=[element])
                    element += 1
                row -= 1
                col += 1


if st.session_state.current_state == 3:

    col1, col2 = st.columns([5, 1])
    with col2:
        reset = st.button("Reset", type="tertiary")
        if reset:
            st.session_state.current_state = 1
            st.session_state.has_clause = False
            st.session_state.first_clause = None
            st.session_state.second_clause = None
            st.session_state.model = None
            st.session_state.clauses = None
            st.rerun()

    with col1:        
        # Display the two clauses being resolved
        clause1 = st.session_state.model.get_clauses()[st.session_state.first_clause]
        clause2 = st.session_state.model.get_clauses()[st.session_state.second_clause]
        st.write(f"Resolving: {clause1} and {clause2}")

        st.write("Select the literal to resolve on:")
        literals = st.session_state.model.get_literal_negation_pairs(st.session_state.first_clause, st.session_state.second_clause)
        for literal in literals:
            def click_literal(lit=literal):
                st.session_state.model.resolve(st.session_state.first_clause, st.session_state.second_clause, lit)
                st.session_state.clauses = st.session_state.model.get_clauses()
                st.session_state.current_state = 2
                st.session_state.has_clause = False
                if any(len(c.get_literals()) == 0 for c in st.session_state.clauses):
                        st.session_state.current_state = 4

            st.button(f"{literal}", key=f"literal_{literal}", on_click=click_literal)

if st.session_state.current_state == 4:
    st.write("Contradiction found, proof complete!")
    st.write("Proof of resolution steps:")
    proof = st.session_state.model.get_proof()
    st.text(proof)
    reset = st.button("Reset")
    if reset:
        st.session_state.current_state = 1
        st.session_state.has_clause = False
        st.session_state.first_clause = None
        st.session_state.second_clause = None
        st.session_state.model = None
        st.session_state.clauses = None
        st.rerun()

