import logging
from ollama import AsyncClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMClient:
    """
    A client to interact with a local large language model (LLM) using asynchronous requests.

    Attributes:
        client (AsyncClient): Asynchronous client for interacting with the LLM.
        model (str): The name of the LLM model to use.
        options (dict): Options for controlling the generation behavior, such as temperature and max tokens.
    """
    def __init__(self, model: str, options=None):
        self.client = AsyncClient(host="http://ollama:11434")
        self.model = model or 'llama3.2'
        self.options = options or {'temperature': 0.7, 'max_tokens': 150}

    async def generate_response(self, prompt: str, response_format):
        """Generate an answers using the local LLM."""
        return await self.client.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}],
            format=response_format,  # Use Pydantic to generate the schema
            options=self.options  # Make responses more deterministic
        )
