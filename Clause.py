from Literal import Literal

class Clause:
        """Inner class representing a Clause (a set of Literals)"""
        
        def __init__(self, literals: set = None, leftParent = None, rightParent = None):
            """
            Initialize a Clause with a set of Literals.
            
            Args:
                literals: Set of Literal objects (defaults to empty set)
                leftParent: Optional Clause representing the left parent in a resolution
                rightParent: Optional Clause representing the right parent in a resolution
            """
            self.__literals = literals if literals is not None else set()
            self.__leftParent = leftParent
            self.__rightParent = rightParent
    
    
        def get_parents(self) -> tuple:
            """Return a tuple of the left and right parent Clauses (or None if not applicable)"""
            return (self.__leftParent, self.__rightParent)

        def get_literals(self) -> set:
            """Get the set of literals in this clause"""
            return self.__literals.copy()
        
        def __repr__(self) -> str:
            return f"{{{', '.join(str(lit) for lit in self.__literals)}}}"
        
        def __eq__(self, other) -> bool:
            """Check equality between two Clauses"""
            if not isinstance(other, Clause):
                return False
            return self.__literals == other.__literals
        
        def __hash__(self) -> int:
            """Make Clause hashable for use in sets"""
            return hash(frozenset(self.__literals))
        
        @staticmethod
        def resolve(clause1: 'Clause', clause2: 'Clause', literal: 'Literal') -> 'Clause':
            """
            Resolve two clauses on a given literal.
            
            Args:
                clause1: First clause
                clause2: Second clause
                literal: The literal to resolve on
                
            Returns:
                A new Clause containing all literals from both clauses except the literal and its negation
                (unless they appear in both clauses, in which case they are kept)
                
            Raises:
                ValueError: If the literal doesn't appear as positive in one clause and negative in the other
            """
            literals1 = clause1.get_literals()
            literals2 = clause2.get_literals()
            
            # Check if literal is in clause1 and its negation is in clause2, or vice versa
            # Create lookup maps for efficiency
            lit_map1 = {(lit.letter, lit.is_negated): lit for lit in literals1}
            lit_map2 = {(lit.letter, lit.is_negated): lit for lit in literals2}
            
            lit_key = (literal.letter, literal.is_negated)
            neg_key = (literal.letter, not literal.is_negated)
            
            literal_in_clause1 = lit_key in lit_map1
            negated_in_clause2 = neg_key in lit_map2
            literal_in_clause2 = lit_key in lit_map2
            negated_in_clause1 = neg_key in lit_map1
            
            if not ((literal_in_clause1 and negated_in_clause2) or (literal_in_clause2 and negated_in_clause1)):
                raise ValueError(
                    f"Cannot resolve on literal {literal}: "
                    f"literal must appear positive in one clause and negative in the other"
                )
            
            # Create the resolvent by combining both sets and removing literals appropriately
            resolvent_literals = set()
            
            # If literal_in_clause1 and negated_in_clause2
            if literal_in_clause1 and negated_in_clause2:
                # Keep literals from clause1 except the literal being resolved (unless it's also in clause2)
                for lit in literals1:
                    if lit.letter != literal.letter or lit in literals2:
                        resolvent_literals.add(lit)
                
                # Keep literals from clause2 except the negated literal being resolved (unless it's also in clause1)
                for lit in literals2:
                    if lit.letter != literal.letter or lit in literals1:
                        resolvent_literals.add(lit)
            
            # If literal_in_clause2 and negated_in_clause1
            elif literal_in_clause2 and negated_in_clause1:
                # Keep literals from clause2 except the literal being resolved (unless it's also in clause1)
                for lit in literals2:
                    if lit.letter != literal.letter or lit in literals1:
                        resolvent_literals.add(lit)
                
                # Keep literals from clause1 except the negated literal being resolved (unless it's also in clause2)
                for lit in literals1:
                    if lit.letter != literal.letter or lit in literals2:
                        resolvent_literals.add(lit)
            
            return Clause(resolvent_literals, clause1, clause2)
        
        @staticmethod
        def parse(s: str) -> 'Clause':
            """
            Parse a string and return the corresponding Clause object.
            
            Expected format:
                - Space or comma-separated literals: "A B ~C" or "{A, B, ~C}" or similar variations
                - Each literal should be in the format accepted by Literal.parse()
            
            Args:
                s: String to parse
                
            Returns:
                A Clause object containing the parsed literals
                
            Raises:
                ValueError: If the string is not in the correct format or contains invalid literals
            """
            if not isinstance(s, str):
                raise ValueError(f"parse() requires a string, got: {type(s).__name__}")
            
            # Remove common delimiters like braces, parentheses, and brackets
            cleaned = s.strip()
            if cleaned.startswith('{') and cleaned.endswith('}'):
                cleaned = cleaned[1:-1]
            elif cleaned.startswith('(') and cleaned.endswith(')'):
                cleaned = cleaned[1:-1]
            elif cleaned.startswith('[') and cleaned.endswith(']'):
                cleaned = cleaned[1:-1]
            
            if not cleaned:
                raise ValueError("parse() requires a non-empty string after removing delimiters")
            
            # Split by common delimiters (spaces, commas, or both)
            literals_set = set()
            
            cleaned = cleaned.replace('∨', ' ').replace(',', ' ')
            literal_strings = [part.strip() for part in cleaned.split()]
            
            for literal_str in literal_strings:
                if not literal_str:  # Skip empty strings
                    continue
                try:
                    literal = Literal.parse(literal_str)
                    literals_set.add(literal)
                except ValueError as e:
                    raise ValueError(f"Invalid literal in clause: {e}")
            
            if not literals_set:
                raise ValueError("parse() resulted in an empty clause with no valid literals")
            
            return Clause(literals_set)
