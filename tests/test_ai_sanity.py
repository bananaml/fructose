from fructose import Fructose
AI = Fructose()

# In all cases, we assert the return type

# In trivial cases that the LLM shouldn't mess up on, we assert the return value. 
# NOTE: this adds flakiness to the tests. But Fructose would be a useless package if we couldn't trust trivial cases. 


# ----
# Type - to - Type tests

def test_str2str():
    @AI()
    def echo(words: str) -> str:
        """
        Repeat the input string back to the user.
        """
    
    res = echo("onomatopoeia")
    assert type(res) == str
    assert res == "onomatopoeia"
    

def test_str2int():
    @AI()
    def len_str(words: str) -> int:
        """
        Return the length of the input string.
        """
    
    res = len_str("onomatopoeia")
    assert type(res) == int


def test_none2int():
    @AI()
    def none2int() -> int:
        """
        Return the integer 42.
        """
    
    res = none2int()
    assert res == 42
    assert type(res) == int

def test_none2str():
    @AI()
    def none2str() -> str:
        """
        Return the string "42".
        """
    
    res = none2str()
    assert res == "42"
    assert type(res) == str

def test_none2float():
    @AI()
    def none2float() -> float:
        """
        Return the float 42.0.
        """
    
    res = none2float()
    assert res == 42.0
    assert type(res) == float

def test_none2bool():
    @AI()
    def none2bool() -> bool:
        """
        Return the boolean True.
        """
    
    res = none2bool()
    assert res == True
    assert type(res) == bool

def test_bool2bool():
    @AI(debug=True)
    def bool2bool(boolean: bool) -> bool:
        """
        Return the input boolean value.
        """
    
    res = bool2bool(True)
    assert res == True
    assert type(res) == bool

    res = bool2bool(False)
    assert res == False
    assert type(res) == bool

def test_bool2int():
    @AI()
    def bool2int(boolean: bool) -> int:
        """
        Return an integer, 1 if the input is True, 0 if the input is False.
        Valid return values are 1 and 0.
        """
    
    res = bool2int(True)
    assert res == 1
    assert type(res) == int

    res = bool2int(False)
    assert res == 0
    assert type(res) == int

def test_bool2str():
    @AI()
    def bool2str(boolean: bool) -> str:
        """
        Return the string "TRUE" if the input is True, "FALSE" if the input is False. It must be in all caps.
        """
    
    res = bool2str(True)
    assert res == "TRUE"
    assert type(res) == str

    res = bool2str(False)
    assert res == "FALSE"
    assert type(res) == str

def test_listint2int():
    @AI()
    def listint2listint(numbers: list[int]) -> int:
        """
        Return the first integer in the list.
        """
    
    res = listint2listint([1, 2, 3])
    assert res == 1
    assert type(res) == int


# ----
# Mixed Args KWArgs tests

def test_kwargs():
    @AI()
    def logical_and(bool1: bool, bool2: bool) -> bool:
        """
        Return the logical AND of the two input booleans.
        """

    res = logical_and(bool1 = True, bool2 = False)
    assert res == False
    assert type(res) == bool

def test_mixed_order_kwargs():
    @AI()
    def logical_and(bool1: bool, bool2: bool) -> bool:
        """
        Return the logical AND of the two input booleans.
        """

    res = logical_and(bool2 = False, bool1 = True)
    assert res == False
    assert type(res) == bool

def test_mixed_positional_kwargs():
    @AI()
    def logical_and(bool1: bool, bool2: bool) -> bool:
        """
        Return the logical AND of the two input booleans.
        """
        
    # mixed positional and kwargs
    res = logical_and(True, bool2 = False)
    assert res == False
    assert type(res) == bool