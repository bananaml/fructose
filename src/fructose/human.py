from .ai import Fructose, get_base_template_env
import openai

import logging

logging.basicConfig(level=logging.DEBUG)

DEFAULT_MODEL = "gpt-3.5-turbo"
HUMAN_BASE_URL = "http://localhost:3000"

class Sucrose(Fructose):
    def __init__(self, client=None, model=DEFAULT_MODEL, system_template_path=None, chain_of_thought_template_path=None, debug=False):
        super().__init__(
            client=openai.Client(
                api_key="not-needed",
                base_url=HUMAN_BASE_URL,
                max_retries=1,
            ), 
            model=model,
            system_template_path=get_base_template_env().get_template("human_prompt.jinja"), 
            chain_of_thought_template_path=chain_of_thought_template_path, 
            debug=debug
        )
