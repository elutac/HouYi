import dataclasses
import json

import requests

from constant.prompt_injection import PromptInjection


@dataclasses.dataclass
class ConnectorHarness:
    name: str
    site_url: str
    endpoint_url: str
    application_document: str

    def run_harness(self, prompt_injection: PromptInjection):
        data = {
            "cvText": prompt_injection.get_attack_prompt()
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(self.endpoint_url, json=data, headers=headers)

        print(response.text)

        return response.text
    