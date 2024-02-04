from fructose import AI

# In all cases, we assert the return type

# In trivial cases that the LLM shouldn't mess up on, we assert the return value. 
# NOTE: this adds flakiness to the tests.
# Fructose would be a useless package if we couldn't trust trivial cases. 

def test_str2str():
    @AI()
    def echo(words: str) -> str:
        """
        Repeat the input string back to the user.
        """
    
    res = echo("onomatopoeia")
    assert type(res) == str
    assert res == "onomatopoeia" # not deterministic, but trivial LLM task
    

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
        Echo the input boolean as the output boolean. True -> True, False -> False. Don't overthink it.
        """
    
    res = bool2bool(True)
    assert res == True
    assert type(res) == bool

    res = bool2bool(False)
    assert res == False
    assert type(res) == bool