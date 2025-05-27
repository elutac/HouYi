import dataclasses
import json
import requests
import sys
import os
import time
from typing import Optional

# Add backend directory to Python path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, backend_path)

from constant.prompt_injection import PromptInjection
from src.utils.pdf_utils import PDFUtils


@dataclasses.dataclass
class ConnectorHarness:
    name: str
    site_url: str
    endpoint_url: str
    application_document: str
    input_type: str = "text"  # Default to text

    def run_harness(self, prompt_injection: PromptInjection):
        attack_prompt = prompt_injection.get_attack_prompt()
        pdf_path = None

        try:
            # Prepare request based on input type
            if self.input_type.lower() == "pdf":
                print(f"Generating PDF for attack prompt: {attack_prompt[:100]}...")  # Debug output
                
                # Convert text to PDF using the utility
                pdf_path, pdf_content, unique_id = PDFUtils.convert_text_to_pdf(attack_prompt)
                
                # Small delay to ensure file system operations are complete
                time.sleep(0.1)
                
                # Verify PDF exists and has content
                if not os.path.exists(pdf_path):
                    raise Exception(f"PDF {unique_id} file not created at {pdf_path}")
                    
                if not pdf_content:
                    raise Exception(f"PDF {unique_id} content is empty")
                
                print(f"PDF {unique_id} generated successfully: {len(pdf_content)} bytes")  # Debug output
                
                # Prepare multipart form data with the correct field name
                files = {
                    'pdf': (f'{unique_id}.pdf', pdf_content, 'application/pdf')
                }
                data = {}
                headers = {}
                json = {}

                print(f"Sending request to {self.endpoint_url} with PDF {unique_id}")
                
            elif self.input_type.lower() == "json":
                # Prepare JSON data
                json = {
                    "text": attack_prompt
                }
                headers = {
                    "Content-Type": "application/json",
                    "User-Agent": "python-requests/2.30.0"
                }
                data = {}
                files = None

                print(f"Sending request to {self.endpoint_url}")
                
            else:  # Default to text
                data = {
                    "cvText": attack_prompt
                }
                headers = {
                    "Content-Type": "application/json"
                }
                files = None
                json = {}

                print(f"Sending request to {self.endpoint_url}")

            response = requests.post(
                self.endpoint_url,
                data=data,
                headers=headers,
                files=files,
                json=json
            )

            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            return response.text

        except Exception as e:
            print(f"Error in run_harness: {str(e)}")  # Debug output
            raise Exception(f"Error in run_harness: {str(e)}")
            
        finally:
            # Clean up PDF file if it was created
            if pdf_path:
                PDFUtils.cleanup_pdf(pdf_path)
