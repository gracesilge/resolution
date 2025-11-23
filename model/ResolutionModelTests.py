import unittest
import Literal
import Clause
import ResolutionModel


class TestLiteralConstructor(unittest.TestCase):
    """Test cases for the Literal constructor"""
    
    def test_create_positive_literal(self):
        """Test creating a positive literal"""
        lit = Literal.Literal(False, "A")
        self.assertFalse(lit.is_negated)
        self.assertEqual(lit.letter, "A")
    
    def test_create_negated_literal(self):
        """Test creating a negated literal"""
        lit = Literal.Literal(True, "B")
        self.assertTrue(lit.is_negated)
        self.assertEqual(lit.letter, "B")
    
    def test_constructor_lowercase_letter_raises_error(self):
        """Test that lowercase letter raises ValueError"""
        with self.assertRaises(ValueError):
            Literal.Literal(False, "a")
    
    def test_constructor_multiple_letters_raises_error(self):
        """Test that multiple letters raise ValueError"""
        with self.assertRaises(ValueError):
            Literal.Literal(False, "AB")
    
    def test_constructor_empty_string_raises_error(self):
        """Test that empty string raises ValueError"""
        with self.assertRaises(ValueError):
            Literal.Literal(False, "")
    
    def test_constructor_non_letter_raises_error(self):
        """Test that non-letter character raises ValueError"""
        with self.assertRaises(ValueError):
            Literal.Literal(False, "1")
    
    def test_constructor_non_string_raises_error(self):
        """Test that non-string letter raises ValueError"""
        with self.assertRaises(ValueError):
            Literal.Literal(False, 123)


class TestLiteralParse(unittest.TestCase):
    """Test cases for the Literal.parse() static method"""
    
    def test_parse_positive_literal_uppercase(self):
        """Test parsing a positive literal: 'A' should create Literal(False, 'A')"""
        result = Literal.Literal.parse("A")
        expected = Literal.Literal(False, "A")
        
        self.assertEqual(result, expected)
        self.assertFalse(result.is_negated)
        self.assertEqual(result.letter, "A")
    
    def test_parse_positive_literal_lowercase(self):
        """Test parsing lowercase converts to uppercase: 'a' should create Literal(False, 'A')"""
        result = Literal.Literal.parse("a")
        expected = Literal.Literal(False, "A")
        
        self.assertEqual(result, expected)
        self.assertFalse(result.is_negated)
        self.assertEqual(result.letter, "A")
    
    def test_parse_negated_literal_uppercase(self):
        """Test parsing a negated literal: '~B' should create Literal(True, 'B')"""
        result = Literal.Literal.parse("~B")
        expected = Literal.Literal(True, "B")
        
        self.assertEqual(result, expected)
        self.assertTrue(result.is_negated)
        self.assertEqual(result.letter, "B")
    
    def test_parse_negated_literal_lowercase(self):
        """Test parsing negated lowercase: '~b' should create Literal(True, 'B')"""
        result = Literal.Literal.parse("~b")
        expected = Literal.Literal(True, "B")
        
        self.assertEqual(result, expected)
        self.assertTrue(result.is_negated)
        self.assertEqual(result.letter, "B")
    
    def test_parse_multiple_capital_letters(self):
        """Test that parsing multiple letters raises ValueError"""
        with self.assertRaises(ValueError):
            Literal.Literal.parse("AB")
    
    def test_parse_empty_string(self):
        """Test that parsing empty string raises ValueError"""
        with self.assertRaises(ValueError):
            Literal.Literal.parse("")
    
    def test_parse_only_tilde(self):
        """Test that parsing only tilde raises ValueError"""
        with self.assertRaises(ValueError):
            Literal.Literal.parse("~")
    
    def test_parse_number(self):
        """Test that parsing a number raises ValueError"""
        with self.assertRaises(ValueError):
            Literal.Literal.parse("1")
    
    def test_parse_negated_number(self):
        """Test that parsing negated number raises ValueError"""
        with self.assertRaises(ValueError):
            Literal.Literal.parse("~1")
    
    def test_parse_special_character(self):
        """Test that parsing special character raises ValueError"""
        with self.assertRaises(ValueError):
            Literal.Literal.parse("!")
    
    def test_parse_non_string_input(self):
        """Test that parsing non-string input raises ValueError"""
        with self.assertRaises(ValueError):
            Literal.Literal.parse(123)
    
    def test_parse_all_capital_letters(self):
        """Test parsing various capital and lowercase letters"""
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
            result = Literal.Literal.parse(letter)
            self.assertEqual(result.letter, letter.upper())
            self.assertFalse(result.is_negated)
            
            result_negated = Literal.Literal.parse(f"~{letter}")
            self.assertEqual(result_negated.letter, letter.upper())
            self.assertTrue(result_negated.is_negated)


class TestLiteralEquality(unittest.TestCase):
    """Test cases for Literal equality"""
    
    def test_equal_literals(self):
        """Test that identical literals are equal"""
        lit1 = Literal.Literal(False, "A")
        lit2 = Literal.Literal(False, "A")
        self.assertEqual(lit1, lit2)
    
    def test_different_negation_not_equal(self):
        """Test that literals with different negation are not equal"""
        lit1 = Literal.Literal(False, "A")
        lit2 = Literal.Literal(True, "A")
        self.assertNotEqual(lit1, lit2)
    
    def test_different_letter_not_equal(self):
        """Test that literals with different letters are not equal"""
        lit1 = Literal.Literal(False, "A")
        lit2 = Literal.Literal(False, "B")
        self.assertNotEqual(lit1, lit2)
    
    def test_hash_equal_literals(self):
        """Test that equal literals have the same hash"""
        lit1 = Literal.Literal(False, "A")
        lit2 = Literal.Literal(False, "A")
        self.assertEqual(hash(lit1), hash(lit2))


class TestClauseConstructor(unittest.TestCase):
    """Test cases for the Clause constructor"""
    
    def test_create_clause_with_literals(self):
        """Test creating a clause with literals"""
        a = Literal.Literal(False, "A")
        b = Literal.Literal(False, "B")
        literals_set = {a, b}
        
        clause = Clause.Clause(literals_set)
        self.assertEqual(clause.get_literals(), literals_set)
    
    def test_create_clause_empty_set(self):
        """Test creating a clause with an empty set"""
        clause = Clause.Clause(set())
        self.assertEqual(clause.get_literals(), set())
    
    def test_create_clause_default(self):
        """Test creating a clause with default argument"""
        clause = Clause.Clause()
        self.assertEqual(clause.get_literals(), set())
    


class TestClauseParse(unittest.TestCase):
    """Test cases for the Clause.parse() static method"""
    
    def test_parse_single_literal(self):
        """Test parsing a single literal"""
        clause = Clause.Clause.parse("A")
        literals = clause.get_literals()
        self.assertEqual(len(literals), 1)
    
    def test_parse_space_separated_literals(self):
        """Test parsing space-separated literals"""
        clause = Clause.Clause.parse("A B C")
        literals = clause.get_literals()
        self.assertEqual(len(literals), 3)
    
    def test_parse_comma_separated_literals(self):
        """Test parsing comma-separated literals"""
        clause = Clause.Clause.parse("A, B, C")
        literals = clause.get_literals()
        self.assertEqual(len(literals), 3)
    
    def test_parse_with_braces(self):
        """Test parsing with braces"""
        clause = Clause.Clause.parse("{A, B, C}")
        literals = clause.get_literals()
        self.assertEqual(len(literals), 3)
    
    def test_parse_with_parentheses(self):
        """Test parsing with parentheses"""
        clause = Clause.Clause.parse("(A B C)")
        literals = clause.get_literals()
        self.assertEqual(len(literals), 3)
    
    def test_parse_with_brackets(self):
        """Test parsing with brackets"""
        clause = Clause.Clause.parse("[A, B, C]")
        literals = clause.get_literals()
        self.assertEqual(len(literals), 3)
    
    def test_parse_with_negated_literals(self):
        """Test parsing with negated literals"""
        clause = Clause.Clause.parse("A ~B C")
        literals = clause.get_literals()
        self.assertEqual(len(literals), 3)
    
    def test_parse_empty_string_raises_error(self):
        """Test that parsing empty string raises ValueError"""
        with self.assertRaises(ValueError):
            Clause.Clause.parse("")
    
    def test_parse_only_delimiters_raises_error(self):
        """Test that parsing only delimiters raises ValueError"""
        with self.assertRaises(ValueError):
            Clause.Clause.parse("{}")
    
    def test_parse_non_string_raises_error(self):
        """Test that parsing non-string raises ValueError"""
        with self.assertRaises(ValueError):
            Clause.Clause.parse(123)


class TestClauseResolve(unittest.TestCase):
    """Test cases for the Clause.resolve() method"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.q = Literal.Literal(False, "Q")
        self.not_q = Literal.Literal(True, "Q")
        self.r = Literal.Literal(False, "R")
        self.a = Literal.Literal(False, "A")
        self.b = Literal.Literal(False, "B")
        self.not_b = Literal.Literal(True, "B")
        self.c = Literal.Literal(False, "C")
    
    def test_resolve_q_not_q_and_q_r_on_q(self):
        """Test 1 - Resolve {Q, ~Q} and {Q, R} on Q: expected {R, Q}"""
        clause1 = Clause.Clause({self.q, self.not_q})  # {Q, ~Q}
        clause2 = Clause.Clause({self.q, self.r})      # {Q, R}
        
        result = Clause.Clause.resolve(clause1, clause2, self.q)
        expected_literals = {self.r, self.q}
        
        self.assertEqual(result.get_literals(), expected_literals)
    
    def test_resolve_q_not_q_and_not_q_r_on_q(self):
        """Test 2 - Resolve {Q, ~Q} and {~Q, R} on Q: expected {R, ~Q}"""
        clause1 = Clause.Clause({self.q, self.not_q})  # {Q, ~Q}
        clause2 = Clause.Clause({self.not_q, self.r})  # {~Q, R}
        
        result = Clause.Clause.resolve(clause1, clause2, self.q)
        expected_literals = {self.r, self.not_q}
        
        self.assertEqual(result.get_literals(), expected_literals)
    
    def test_resolve_q_not_q_and_q_not_q_on_q(self):
        """Test 3 - Resolve {Q, ~Q} and {Q, ~Q} on Q: expected {Q, ~Q}"""
        clause1 = Clause.Clause({self.q, self.not_q})  # {Q, ~Q}
        clause2 = Clause.Clause({self.q, self.not_q})  # {Q, ~Q}
        
        result = Clause.Clause.resolve(clause1, clause2, self.q)
        expected_literals = {self.q, self.not_q}
        
        self.assertEqual(result.get_literals(), expected_literals)
    
    def test_resolve_q_not_q_and_q_r_on_not_q(self):
        """Test 4 - Resolve {Q, ~Q} and {Q, R} on ~Q: expected {R, Q}"""
        clause1 = Clause.Clause({self.q, self.not_q})  # {Q, ~Q}
        clause2 = Clause.Clause({self.q, self.r})      # {Q, R}
        
        result = Clause.Clause.resolve(clause1, clause2, self.not_q)
        expected_literals = {self.r, self.q}
        
        self.assertEqual(result.get_literals(), expected_literals)
    
    def test_resolve_a_not_b_and_b_c_on_b(self):
        """Test 5 - Resolve {A, ~B} and {B, C} on B: expected {A, C}"""
        clause1 = Clause.Clause({self.a, self.not_b})  # {A, ~B}
        clause2 = Clause.Clause({self.b, self.c})      # {B, C}
        
        result = Clause.Clause.resolve(clause1, clause2, self.b)
        expected_literals = {self.a, self.c}
        
        self.assertEqual(result.get_literals(), expected_literals)
    
    def test_resolve_b_and_not_b_on_b(self):
        """Test 6 - Resolve {B} and {~B} on B: expected {} (empty clause)"""
        clause1 = Clause.Clause({self.b})      # {B}
        clause2 = Clause.Clause({self.not_b})  # {~B}
        
        result = Clause.Clause.resolve(clause1, clause2, self.b)
        expected_literals = set()  # Empty set
        
        self.assertEqual(result.get_literals(), expected_literals)
    
    def test_resolve_incompatible_clauses_raises_error(self):
        """Test that resolving incompatible clauses raises ValueError"""
        clause1 = Clause.Clause({self.a})  # {A}
        clause2 = Clause.Clause({self.b})  # {B}
        
        with self.assertRaises(ValueError):
            Clause.Clause.resolve(clause1, clause2, self.a)


class TestResolutionModelConstructor(unittest.TestCase):
    """Test cases for the ResolutionModel constructor"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.a = Literal.Literal(False, "A")
        self.b = Literal.Literal(False, "B")
        self.clause1 = Clause.Clause({self.a})
        self.clause2 = Clause.Clause({self.b})
    
    def test_create_resolution_model(self):
        """Test creating a resolution model with clauses"""
        clauses = [self.clause1, self.clause2]
        model = ResolutionModel.ResolutionModel(clauses)
        
        self.assertEqual(model.get_clauses(), clauses)
    
    def test_create_resolution_model_empty_list_raises_error(self):
        """Test that empty clause list raises ValueError"""
        with self.assertRaises(ValueError):
            ResolutionModel.ResolutionModel([])
    
    def test_create_resolution_model_non_list_raises_error(self):
        """Test that non-list raises TypeError"""
        with self.assertRaises(TypeError):
            ResolutionModel.ResolutionModel("not a list")


class TestResolutionModelGetClauses(unittest.TestCase):
    """Test cases for the ResolutionModel.get_clauses() method"""
    
    def test_get_clauses(self):
        """Test getting clauses from model"""
        a = Literal.Literal(False, "A")
        clause1 = Clause.Clause({a})
        
        model = ResolutionModel.ResolutionModel([clause1])
        clauses = model.get_clauses()
        
        self.assertEqual(clauses, [clause1])


class TestResolutionModelResolve(unittest.TestCase):
    """Test cases for the ResolutionModel.resolve() method"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.q = Literal.Literal(False, "Q")
        self.not_q = Literal.Literal(True, "Q")
        self.r = Literal.Literal(False, "R")
        
        self.clause1 = Clause.Clause({self.q, self.not_q})  # {Q, ~Q}
        self.clause2 = Clause.Clause({self.q, self.r})      # {Q, R}
        self.clause3 = Clause.Clause({self.not_q, self.r})  # {~Q, R}
    
    def test_resolve_clauses_by_index_appends_result(self):
        """Test resolving clauses by index appends result to clauses list"""
        model = ResolutionModel.ResolutionModel([self.clause1, self.clause2])
        initial_length = len(model.get_clauses())
        
        model.resolve(0, 1, self.q)
        
        # Check that a new clause was appended
        self.assertEqual(len(model.get_clauses()), initial_length + 1)
        
        # Check the appended clause is the expected result
        result_clause = model.get_clauses()[-1]
        expected_literals = {self.r, self.q}
        self.assertEqual(result_clause.get_literals(), expected_literals)
    
    def test_resolve_invalid_index1_raises_error(self):
        """Test that invalid index1 raises IndexError"""
        model = ResolutionModel.ResolutionModel([self.clause1, self.clause2])
        
        with self.assertRaises(IndexError):
            model.resolve(5, 1, self.q)
    
    def test_resolve_invalid_index2_raises_error(self):
        """Test that invalid index2 raises IndexError"""
        model = ResolutionModel.ResolutionModel([self.clause1, self.clause2])
        
        with self.assertRaises(IndexError):
            model.resolve(0, 5, self.q)
    
    def test_resolve_negative_index_raises_error(self):
        """Test that negative index raises IndexError"""
        model = ResolutionModel.ResolutionModel([self.clause1, self.clause2])
        
        with self.assertRaises(IndexError):
            model.resolve(-1, 1, self.q)
    
    def test_resolve_multiple_times(self):
        """Test resolving multiple times builds up the clauses list"""
        model = ResolutionModel.ResolutionModel([self.clause1, self.clause2])
        initial_length = len(model.get_clauses())
        
        model.resolve(0, 1, self.q)
        self.assertEqual(len(model.get_clauses()), initial_length + 1)
        
        # Resolve with the new clause
        model.resolve(2, 0, self.not_q)
        self.assertEqual(len(model.get_clauses()), initial_length + 2)


class TestResolutionModelParse(unittest.TestCase):
    """Test cases for the ResolutionModel.parse() static method"""
    
    def test_parse_space_separated_clauses(self):
        """Test parsing space-separated clauses"""
        model = ResolutionModel.ResolutionModel.parse("{A, B} {~B, C}")
        clauses = model.get_clauses()
        
        self.assertEqual(len(clauses), 2)
    
    def test_parse_ampersand_separated_clauses(self):
        """Test parsing clauses separated by & (ampersand)"""
        model = ResolutionModel.ResolutionModel.parse("{A, B} & {~B, C}")
        clauses = model.get_clauses()
        
        self.assertEqual(len(clauses), 2)
    
    def test_parse_logical_and_separated_clauses(self):
        """Test parsing clauses separated by ∧ (logical AND)"""
        model = ResolutionModel.ResolutionModel.parse("{A, B} ∧ {~B, C}")
        clauses = model.get_clauses()
        
        self.assertEqual(len(clauses), 2)
    
    def test_parse_mixed_separators(self):
        """Test parsing with mixed separators"""
        model = ResolutionModel.ResolutionModel.parse("{A} & {B} ∧ {C}")
        clauses = model.get_clauses()
        
        self.assertEqual(len(clauses), 3)
    
    def test_parse_single_clause(self):
        """Test parsing a single clause"""
        model = ResolutionModel.ResolutionModel.parse("{A, B, C}")
        clauses = model.get_clauses()
        
        self.assertEqual(len(clauses), 1)
    
    def test_parse_with_parentheses(self):
        """Test parsing clauses with parentheses"""
        model = ResolutionModel.ResolutionModel.parse("(A B) (B C)")
        clauses = model.get_clauses()
        
        self.assertEqual(len(clauses), 2)
    
    def test_parse_with_brackets(self):
        """Test parsing clauses with brackets"""
        model = ResolutionModel.ResolutionModel.parse("[A, B] [B, C]")
        clauses = model.get_clauses()
        
        self.assertEqual(len(clauses), 2)
    
    def test_parse_with_negated_literals(self):
        """Test parsing with negated literals"""
        model = ResolutionModel.ResolutionModel.parse("{~A, B} & {A, ~C}")
        clauses = model.get_clauses()
        
        self.assertEqual(len(clauses), 2)
    
    def test_parse_complex_expression(self):
        """Test parsing a complex expression"""
        model = ResolutionModel.ResolutionModel.parse("{A, ~B} ∧ {B, C} & {~C, A}")
        clauses = model.get_clauses()
        
        self.assertEqual(len(clauses), 3)
    
    def test_parse_lowercase_literals(self):
        """Test parsing with lowercase literals (should convert to uppercase)"""
        model = ResolutionModel.ResolutionModel.parse("{a, b} {c}")
        clauses = model.get_clauses()
        
        self.assertEqual(len(clauses), 2)
    
    def test_parse_empty_string_raises_error(self):
        """Test that parsing empty string raises ValueError"""
        with self.assertRaises(ValueError):
            ResolutionModel.ResolutionModel.parse("")
    
    def test_parse_only_separators_raises_error(self):
        """Test that parsing only separators raises ValueError"""
        with self.assertRaises(ValueError):
            ResolutionModel.ResolutionModel.parse("& ∧ &")
    
    def test_parse_non_string_raises_error(self):
        """Test that parsing non-string raises TypeError"""
        with self.assertRaises(TypeError):
            ResolutionModel.ResolutionModel.parse(123)
    
    def test_parse_invalid_clause_raises_error(self):
        """Test that invalid clause raises ValueError"""
        with self.assertRaises(ValueError):
            ResolutionModel.ResolutionModel.parse("{A} {invalid!}")
    
    def test_parse_result_is_resolution_model(self):
        """Test that parse returns a ResolutionModel instance"""
        result = ResolutionModel.ResolutionModel.parse("{A} {B}")
        
        self.assertIsInstance(result, ResolutionModel.ResolutionModel)
    
    def test_parse_with_extra_whitespace(self):
        """Test parsing with extra whitespace"""
        model = ResolutionModel.ResolutionModel.parse("  {A, B}   &   {B, C}  ")
        clauses = model.get_clauses()
        
        self.assertEqual(len(clauses), 2)
    
    def test_parse_result_content_correctness(self):
        """Test that parsed model contains correct clauses"""
        model = ResolutionModel.ResolutionModel.parse("{A, B} {B, C}")
        clauses = model.get_clauses()
        
        # First clause should have 2 literals
        self.assertEqual(len(clauses[0].get_literals()), 2)
        # Second clause should have 2 literals
        self.assertEqual(len(clauses[1].get_literals()), 2)


class TestClauseEquality(unittest.TestCase):
    """Test cases for Clause equality and hashing"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.a = Literal.Literal(False, "A")
        self.b = Literal.Literal(False, "B")
        self.not_b = Literal.Literal(True, "B")
        self.c = Literal.Literal(False, "C")
    
    def test_equal_clauses(self):
        """Test that identical clauses are equal"""
        clause1 = Clause.Clause({self.a, self.b})
        clause2 = Clause.Clause({self.a, self.b})
        
        self.assertEqual(clause1, clause2)
    
    def test_different_literals_not_equal(self):
        """Test that clauses with different literals are not equal"""
        clause1 = Clause.Clause({self.a, self.b})
        clause2 = Clause.Clause({self.a, self.c})
        
        self.assertNotEqual(clause1, clause2)
    
    def test_different_size_not_equal(self):
        """Test that clauses with different sizes are not equal"""
        clause1 = Clause.Clause({self.a, self.b})
        clause2 = Clause.Clause({self.a})
        
        self.assertNotEqual(clause1, clause2)
    
    def test_hash_equal_clauses(self):
        """Test that equal clauses have the same hash"""
        clause1 = Clause.Clause({self.a, self.b})
        clause2 = Clause.Clause({self.a, self.b})
        
        self.assertEqual(hash(clause1), hash(clause2))
    
    def test_clauses_in_set(self):
        """Test that equal clauses are treated as same in sets"""
        clause1 = Clause.Clause({self.a, self.b})
        clause2 = Clause.Clause({self.a, self.b})
        clause3 = Clause.Clause({self.b, self.c})
        
        clause_set = {clause1, clause2, clause3}
        self.assertEqual(len(clause_set), 2)  # clause1 and clause2 count as one
    
    def test_clause_not_equal_to_non_clause(self):
        """Test that clause is not equal to non-Clause object"""
        clause = Clause.Clause({self.a})
        
        self.assertNotEqual(clause, "not a clause")
        self.assertNotEqual(clause, 123)
        self.assertNotEqual(clause, None)
    
    def test_empty_clauses_equal(self):
        """Test that empty clauses are equal"""
        clause1 = Clause.Clause()
        clause2 = Clause.Clause()
        
        self.assertEqual(clause1, clause2)
    
    def test_hash_consistency(self):
        """Test that hash is consistent across multiple calls"""
        clause = Clause.Clause({self.a, self.b})
        hash1 = hash(clause)
        hash2 = hash(clause)
        
        self.assertEqual(hash1, hash2)
    
    def test_negated_vs_positive_different(self):
        """Test that clauses with negated vs positive literals are different"""
        clause1 = Clause.Clause({self.b})
        clause2 = Clause.Clause({self.not_b})
        
        self.assertNotEqual(clause1, clause2)


class TestResolutionModelEquality(unittest.TestCase):
    """Test cases for ResolutionModel equality and hashing"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.a = Literal.Literal(False, "A")
        self.b = Literal.Literal(False, "B")
        self.c = Literal.Literal(False, "C")
        
        self.clause1 = Clause.Clause({self.a})
        self.clause2 = Clause.Clause({self.b})
        self.clause3 = Clause.Clause({self.c})
    
    def test_equal_models(self):
        """Test that identical models are equal"""
        model1 = ResolutionModel.ResolutionModel([self.clause1, self.clause2])
        model2 = ResolutionModel.ResolutionModel([self.clause1, self.clause2])
        
        self.assertEqual(model1, model2)
    
    def test_different_clauses_not_equal(self):
        """Test that models with different clauses are not equal"""
        model1 = ResolutionModel.ResolutionModel([self.clause1, self.clause2])
        model2 = ResolutionModel.ResolutionModel([self.clause1, self.clause3])
        
        self.assertNotEqual(model1, model2)
    
    def test_different_order_not_equal(self):
        """Test that models with clauses in different order are not equal"""
        model1 = ResolutionModel.ResolutionModel([self.clause1, self.clause2])
        model2 = ResolutionModel.ResolutionModel([self.clause2, self.clause1])
        
        self.assertNotEqual(model1, model2)
    
    def test_different_size_not_equal(self):
        """Test that models with different sizes are not equal"""
        model1 = ResolutionModel.ResolutionModel([self.clause1, self.clause2])
        model2 = ResolutionModel.ResolutionModel([self.clause1])
        
        self.assertNotEqual(model1, model2)
    
    def test_hash_equal_models(self):
        """Test that equal models have the same hash"""
        model1 = ResolutionModel.ResolutionModel([self.clause1, self.clause2])
        model2 = ResolutionModel.ResolutionModel([self.clause1, self.clause2])
        
        self.assertEqual(hash(model1), hash(model2))
    
    def test_models_in_set(self):
        """Test that equal models are treated as same in sets"""
        model1 = ResolutionModel.ResolutionModel([self.clause1, self.clause2])
        model2 = ResolutionModel.ResolutionModel([self.clause1, self.clause2])
        model3 = ResolutionModel.ResolutionModel([self.clause1, self.clause3])
        
        model_set = {model1, model2, model3}
        self.assertEqual(len(model_set), 2)  # model1 and model2 count as one
    
    def test_model_not_equal_to_non_model(self):
        """Test that model is not equal to non-ResolutionModel object"""
        model = ResolutionModel.ResolutionModel([self.clause1])
        
        self.assertNotEqual(model, "not a model")
        self.assertNotEqual(model, 123)
        self.assertNotEqual(model, None)
    
    def test_hash_consistency(self):
        """Test that hash is consistent across multiple calls"""
        model = ResolutionModel.ResolutionModel([self.clause1, self.clause2])
        hash1 = hash(model)
        hash2 = hash(model)
        
        self.assertEqual(hash1, hash2)
    
    def test_models_in_dict(self):
        """Test that models can be used as dictionary keys"""
        model1 = ResolutionModel.ResolutionModel([self.clause1, self.clause2])
        model2 = ResolutionModel.ResolutionModel([self.clause1, self.clause2])
        
        model_dict = {model1: "value1"}
        model_dict[model2] = "value2"
        
        self.assertEqual(len(model_dict), 1)  # Same model, so only one key
        self.assertEqual(model_dict[model1], "value2")


if __name__ == "__main__":
    unittest.main()



