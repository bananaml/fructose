from fructose.llm_agent import LLMAgent, SystemInstructions, BasicPrompt

system = SystemInstructions("Given a list of words return a word describing the theme")

input_format = list[str]

response_format = str

my_agent = LLMAgent(
    system_template=system,
    prompt=BasicPrompt(),
    input_format=input_format,
    response_format=response_format,
)

result = my_agent([["apple", "banana", "cherry"]])
print(result) # outputs "fruits"

