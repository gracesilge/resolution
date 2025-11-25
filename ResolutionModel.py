from Literal import Literal
from Clause import Clause

class ResolutionModel:
    """Represents a full CNF resolution model consisting of multiple clauses."""
    
    def __init__(self, clauses: list):
        """
        Initialize a ResolutionModel with a list of unique Clauses.
        
        Args:
            clauses: List of Clause objects (must not be empty)
            
        Raises:
            ValueError: If the list is empty
            TypeError: If clauses is not a list
        """
        if not isinstance(clauses, list):
            raise TypeError(f"clauses must be a list, got: {type(clauses).__name__}")
        
        if len(clauses) == 0:
            raise ValueError("clauses list cannot be empty")
        
        if not all(isinstance(c, Clause) for c in clauses):
            raise TypeError("all items in clauses list must be Clause objects")
        
        # Ensure uniqueness while preserving order
        seen = set()
        unique_clauses = []
        for c in clauses:
            if c not in seen:
                unique_clauses.append(c)
                seen.add(c)
        self.__clauses = unique_clauses
    
    def get_clauses(self) -> list:
        """Return a copy of the list of clauses in this resolution model"""
        return self.__clauses.copy()
    
    def __repr__(self) -> str:
        """String representation of the resolution model"""
        return f"ResolutionModel({{{', '.join(str(c) for c in self.__clauses)}}})"
    
    def __eq__(self, other) -> bool:
        """Check equality between two ResolutionModels"""
        if not isinstance(other, ResolutionModel):
            return False
        return self.__clauses == other.__clauses
    
    def __hash__(self) -> int:
        """Make ResolutionModel hashable for use in sets"""
        return hash(tuple(self.__clauses))
    
    def num_clauses(self) -> int:
        """Get the number of clauses in this model"""
        return len(self.__clauses)
    
    def resolve(self, index1: int, index2: int, literal: Literal) -> None:
        """
        Resolve two clauses in the model on a given literal.
        
        Args:
            index1: Index of the first clause
            index2: Index of the second clause
            literal: The literal to resolve on
            
       Raises:
            IndexError: If either index is out of range
            TypeError: If literal is not a Literal object
            ValueError: If the clauses cannot be resolved on the given literal
        """
        if not isinstance(literal, Literal):
            raise TypeError(f"literal must be a Literal object, got: {type(literal).__name__}")
        
        if index1 < 0 or index1 >= len(self.__clauses):
            raise IndexError(f"index1 {index1} is out of range for clauses list of length {len(self.__clauses)}")
        
        if index2 < 0 or index2 >= len(self.__clauses):
            raise IndexError(f"index2 {index2} is out of range for clauses list of length {len(self.__clauses)}")
        
        clause1 = self.__clauses[index1]
        clause2 = self.__clauses[index2]
        new_clause = Clause.resolve(clause1, clause2, literal)
        if new_clause not in self.__clauses:
            self.__clauses.append(new_clause)
    
    def numResolveLiterals(self, index1: int, index2: int) -> int:
        """
        Return the number of literal-negation pairs between the clauses at index1 and index2.
        Raises IndexError for invalid indices.
        """
        if index1 < 0 or index1 >= len(self.__clauses):
            raise IndexError(f"index1 {index1} is out of range for clauses list of length {len(self.__clauses)}")
        if index2 < 0 or index2 >= len(self.__clauses):
            raise IndexError(f"index2 {index2} is out of range for clauses list of length {len(self.__clauses)}")

        clause1 = self.__clauses[index1]
        clause2 = self.__clauses[index2]
        literals1 = clause1.get_literals()
        literals2 = clause2.get_literals()

        # Find all literal-negation pairs
        pairs = 0
        for lit1 in literals1:
            for lit2 in literals2:
                if lit1.letter == lit2.letter and lit1.is_negated != lit2.is_negated:
                    pairs += 1
        return pairs

    def getEasyLiteral(self, index1: int, index2: int) -> Literal:
        """
        Returns a literal from clause at index1 that has its negation in clause at index2,
        or vice versa. Raises IndexError for invalid indices. Returns the first such literal found.
        Raises ValueError if no such literal exists.
        """
        if index1 < 0 or index1 >= len(self.__clauses):
            raise IndexError(f"index1 {index1} is out of range for clauses list of length {len(self.__clauses)}")
        if index2 < 0 or index2 >= len(self.__clauses):
            raise IndexError(f"index2 {index2} is out of range for clauses list of length {len(self.__clauses)}")

        clause1 = self.__clauses[index1]
        clause2 = self.__clauses[index2]
        literals1 = clause1.get_literals()
        literals2 = clause2.get_literals()

        for lit1 in literals1:
            for lit2 in literals2:
                if lit1.letter == lit2.letter and lit1.is_negated != lit2.is_negated:
                    return lit1
        for lit2 in literals2:
            for lit1 in literals1:
                if lit2.letter == lit1.letter and lit2.is_negated != lit1.is_negated:
                    return lit2
        raise ValueError("No literal-negation pair found between the two clauses.")

    def get_literal_negation_pairs(self, index1: int, index2: int) -> list:
        """
        Returns a list of non-negated literals from clause at index1 or index2
        that have their negation in the other clause. Raises IndexError for invalid indices.
        """
        if index1 < 0 or index1 >= len(self.__clauses):
            raise IndexError(f"index1 {index1} is out of range for clauses list of length {len(self.__clauses)}")
        if index2 < 0 or index2 >= len(self.__clauses):
            raise IndexError(f"index2 {index2} is out of range for clauses list of length {len(self.__clauses)}")

        clause1 = self.__clauses[index1]
        clause2 = self.__clauses[index2]
        literals1 = clause1.get_literals()
        literals2 = clause2.get_literals()

        pairs = []
        # Only add the non-negated literal for each pair
        for lit1 in literals1:
            for lit2 in literals2:
                if lit1.letter == lit2.letter and lit1.is_negated != lit2.is_negated:
                    if not lit1.is_negated:
                        pairs.append(lit1)
                    elif not lit2.is_negated:
                        pairs.append(lit2)
        # Remove duplicates (by letter)
        unique_pairs = []
        seen = set()
        for lit in pairs:
            key = lit.letter
            if key not in seen:
                unique_pairs.append(lit)
                seen.add(key)
        return unique_pairs

    @staticmethod
    def parse(s: str) -> 'ResolutionModel':
        """
        Parse a string and return the corresponding ResolutionModel object.

        Accepts formats like:
            - "{C, D}, {A, ~B}"
            - "{A, B} & {~B, C}"
            - "(A B) ∧ (~B C)"
            - "{{A, B}, {C, D}}"
            - Each clause should be in the format accepted by Clause.parse()

        Args:
            s: String to parse

        Returns:
            A ResolutionModel object containing the parsed clauses

        Raises:
            ValueError: If the string is not in the correct format or contains invalid clauses
            TypeError: If the input is not a string
        """
        if not isinstance(s, str):
            raise TypeError(f"parse() requires a string, got: {type(s).__name__}")

        cleaned = s.strip()
        if not cleaned:
            raise ValueError("parse() requires a non-empty string")

        import re
        # Try to find all substrings that look like { ... }
        clause_strings = re.findall(r'\{[^}]*\}', cleaned)

        if not clause_strings:
            # Try to find all substrings that look like ( ... )
            clause_strings = re.findall(r'\([^)]*\)', cleaned)

        if not clause_strings:
            # Try to find all substrings that look like [ ... ]
            clause_strings = re.findall(r'\[[^\]]*\]', cleaned)    

        if not clause_strings:
            # If no {...}, [ ... ], or (...) found, fall back to previous splitting logic
            cleaned = cleaned.replace('&', ' ').replace('∧', ' ')
            clause_strings = cleaned.split()

        if not clause_strings:
            raise ValueError("parse() resulted in no valid clauses")

        clauses = []
        for clause_str in clause_strings:
            clause_str = clause_str.strip()
            if not clause_str:
                continue
            try:
                clause = Clause.parse(clause_str)
                if clause not in clauses:
                    clauses.append(clause)
            except ValueError as e:
                raise ValueError(f"Invalid clause in model: {e}")

        if not clauses:
            raise ValueError("parse() resulted in no valid clauses")

        return ResolutionModel(clauses)
