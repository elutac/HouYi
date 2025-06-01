import dataclasses
import os
import sys
from constant.prompt_injection import PromptInjection

# Add backend directory to Python path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, backend_path)
from src.utils.request_utils import RequestUtils

@dataclasses.dataclass
class ConnectorHarness:
    endpoint_url: str
    content_type: str = "text"

    def run_harness(self, prompt_injection: PromptInjection) -> str:
        """Run the harness with the given prompt injection"""
        attack_prompt = prompt_injection.get_attack_prompt()
        
        try:
            return RequestUtils.send_request(
                self.endpoint_url,
                attack_prompt,
                self.content_type
            )
        except Exception as e:
            print(f"Error in run_harness: {str(e)}")  # Debug output
            raise
