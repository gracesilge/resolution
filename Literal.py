class Literal:
    """Class representing a Literal"""
    
    def __init__(self, is_negated: bool, letter: str):
        """
        Initialize a Literal with private variables.
        
        Args:
            is_negated: Boolean indicating if the literal is negated
            letter: String representing the letter (must be a single capital letter)
            
        Raises:
            ValueError: If letter is not exactly one capital letter
        """
        if not isinstance(letter, str) or len(letter) != 1 or not letter.isalpha() or not letter.isupper():
            raise ValueError(f"letter must be a single capital letter, got: {letter}")
        
        self.__is_negated = is_negated
        self.__letter = letter
    
    @property
    def is_negated(self) -> bool:
        """Get the negation status of the literal"""
        return self.__is_negated
    
    @property
    def letter(self) -> str:
        """Get the letter of the literal"""
        return self.__letter
    
    def __repr__(self) -> str:
        negation_symbol = "~" if self.__is_negated else ""
        return f"{negation_symbol}{self.__letter}"
    
    def __eq__(self, other) -> bool:
        """Check equality between two Literals"""
        if not isinstance(other, Literal):
            return False
        return self.__is_negated == other.__is_negated and self.__letter == other.__letter
    
    def __hash__(self) -> int:
        """Make Literal hashable for use in sets"""
        return hash((self.__is_negated, self.__letter))
    
    @staticmethod
    def parse(s: str) -> 'Literal':
        """
        Parse a string and return the corresponding Literal.
        
        Expected format:
            - Single letter (uppercase or lowercase): "A", "a", "B", etc. (positive literal)
            - Tilde followed by letter: "~A", "~a", "~B", etc. (negated literal)
            - Lowercase letters are automatically converted to uppercase
        
        Args:
            s: String to parse
            
        Returns:
            A Literal object corresponding to the parsed string
            
        Raises:
            ValueError: If the string is not in the correct format
        """
        if not isinstance(s, str):
            raise ValueError(f"parse() requires a string, got: {type(s).__name__}")
        
        if len(s) == 0:
            raise ValueError("parse() requires a non-empty string")
        
        # Check if the literal is negated
        is_negated = False
        letter_part = s
        
        if s[0] == '~':
            is_negated = True
            letter_part = s[1:]
        
        # Validate the letter part (must be alphabetic)
        if len(letter_part) != 1 or not letter_part.isalpha():
            raise ValueError(f"Invalid literal format: '{s}'. Expected format: 'A' or '~A' where A is a letter")
        
        # Convert to uppercase
        letter_part = letter_part.upper()
        
        return Literal(is_negated, letter_part)