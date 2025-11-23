def width(n: int) -> int:
    """
    Calculate the width value based on the given integer n.
    
    Args:
        n: Input integer
        
    Returns:
        Width value based on the pattern
        
    Raises:
        ValueError: If n is less than 0
    """
    if n < 0:
        raise ValueError("n must be >= 0")
    
    # Pattern: pairs of widths each have 2*(even width of pair) numbers
    # w=2,3: 2+2 = 4 numbers (cumulative: 4)
    # w=4,5: 4+4 = 8 numbers (cumulative: 12)
    # w=6,7: 6+6 = 12 numbers (cumulative: 24)
    
    
    # Find which pair (width, width+1) contains n
    cumulative = 0
    width_val = 2
    
    while True:
        
        # Check if n falls in first width of pair
        if cumulative + width_val >= n:
            return width_val
        
        cumulative += width_val
        
        # Check if n falls in second width of pair
        if cumulative + width_val >= n:
            return width_val + 1
        
        cumulative += width_val
        width_val += 2


# Test cases
if __name__ == "__main__":
    test_cases = [
        (0, 2), (1, 2), (2, 2),
        (3, 3), (4, 3),
        (5, 4), (6, 4), (7, 4), (8, 4),
        (9, 5), (10, 5), (11, 5), (12, 5),
        (13, 6), (14, 6), (15, 6), (16, 6), (17, 6), (18, 6),
        (19, 7), (20, 7), (21, 7), (22, 7), (23, 7), (24, 7),
        (25, 8), (26, 8), (27, 8), (28, 8), (29, 8), (30, 8), (31, 8), (32, 8), 
        (33, 9), (34, 9), (35, 9), (36, 9), (37, 9), (38, 9), (39, 9), (40, 9),
        (41, 10), (42, 10), (43, 10), (44, 10), (45, 10), (46, 10), (47, 10), (48, 10), (49, 10), (50, 10),
        (51, 11), (52, 11), (53, 11), (54, 11), (55, 11), (56, 11), (57, 11), (58, 11), (59, 11), (60, 11),
    ]
    
    print("Testing width function:")
    all_pass = True
    for n, expected in test_cases:
        result = width(n)
        status = "✓" if result == expected else "✗"
        if result != expected:
            all_pass = False
        print(f"{status} width({n}) = {result} (expected {expected})")
    
    print(f"\nAll tests passed: {all_pass}")
