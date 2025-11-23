from Literal import Literal
from Clause import Clause

class ResolutionModel:
    """Represents a full CNF resolution model consisting of multiple clauses."""
    
    def __init__(self, clauses: list):
        """
        Initialize a ResolutionModel with a list of Clauses.
        
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
        
        self.__clauses = clauses
    
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
        
        self.__clauses.append(Clause.resolve(clause1, clause2, literal))
    
    @staticmethod
    def parse(s: str) -> 'ResolutionModel':
        """
        Parse a string and return the corresponding ResolutionModel object.
        
        Expected format:
            - Multiple clauses separated by whitespace, '&', or '∧'
            - Each clause should be in the format accepted by Clause.parse()
            - Supports nested delimiters: {{A, B}, {C, D}} or ((A B) (C D))
            - Example: "{A, B} & {~B, C}" or "(A B) ∧ (~B C)" or "{{A, B}, {C, D}}"
        
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
        
        # Check if the entire string is wrapped in outer delimiters
        # If so, remove them first
        if (cleaned.startswith('{') and cleaned.endswith('}')) or \
           (cleaned.startswith('(') and cleaned.endswith(')')) or \
           (cleaned.startswith('[') and cleaned.endswith(']')):
            # Check if these are matching outer delimiters
            outer_open = cleaned[0]
            outer_close = cleaned[-1]
            
            # Define matching pairs
            matching = {'{': '}', '(': ')', '[': ']'}
            
            if outer_open in matching and matching[outer_open] == outer_close:
                # Remove outer delimiters and check if they're truly outer
                inner = cleaned[1:-1].strip()
                
                # Verify these are actual outer delimiters by checking bracket balance
                if is_balanced_and_outer(cleaned):
                    cleaned = inner
        
        if not cleaned.strip():
            raise ValueError("parse() requires a non-empty string after removing delimiters")
        
        # Split by &, ∧, or whitespace
        # First replace & and ∧ with a common delimiter
        cleaned = cleaned.replace('&', ' ').replace('∧', ' ')
        
        # Split by whitespace while respecting nested delimiters
        clause_strings = smart_split(cleaned)
        
        if not clause_strings:
            raise ValueError("parse() resulted in no valid clauses")
        
        # Parse each clause
        clauses = []
        for clause_str in clause_strings:
            clause_str = clause_str.strip()
            if not clause_str:
                continue
            try:
                clause = Clause.parse(clause_str)
                clauses.append(clause)
            except ValueError as e:
                raise ValueError(f"Invalid clause in model: {e}")
        
        if not clauses:
            raise ValueError("parse() resulted in no valid clauses")
        
        return ResolutionModel(clauses)


def is_balanced_and_outer(s: str) -> bool:
    """
    Check if the outer delimiters are truly outer (balanced at the outermost level).
    
    Args:
        s: String with potential delimiters
        
    Returns:
        True if outer delimiters are balanced at the top level
    """
    if len(s) < 2:
        return False
    
    matching = {'{': '}', '(': ')', '[': ']'}
    open_char = s[0]
    close_char = s[-1]
    
    if open_char not in matching or matching[open_char] != close_char:
        return False
    
    # Check if the closing delimiter matches at the correct depth
    depth = 0
    for i, char in enumerate(s):
        if char in matching:
            depth += 1
        elif char in matching.values():
            depth -= 1
        
        # If depth reaches 0 before the end, outer delimiters don't match
        if depth == 0 and i < len(s) - 1:
            return False
    
    return depth == 0


def smart_split(s: str) -> list:
    """
    Split a string by whitespace while respecting nested delimiters.
    
    Args:
        s: String to split
        
    Returns:
        List of clause strings
    """
    matching = {'{': '}', '(': ')', '[': ']'}
    reverse_matching = {v: k for k, v in matching.items()}
    
    clauses = []
    current = []
    depth = 0
    
    for char in s:
        if char in matching:
            depth += 1
            current.append(char)
        elif char in reverse_matching:
            depth -= 1
            current.append(char)
        elif char.isspace() and depth == 0:
            if current:
                clauses.append(''.join(current))
                current = []
        else:
            current.append(char)
    
    if current:
        clauses.append(''.join(current))
    
    return clauses
