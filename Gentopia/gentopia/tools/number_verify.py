# Importing necessary libraries:
from gentopia.tools.basetool import *
# Importing for making HTTP requests:
import urllib.request
# For parsing JSON responses:
import json
from typing import Any, Optional, Type

class NumVerifyArgs(BaseModel):
    # phone_number: the phone number to be validated
    phone_number: str
    # country_code: Optional country code for national numbers (e.g., 'US')
    country_code: Optional[str] = None

class NumVerify(BaseTool):
    """A Tool for retrieving phone number details using the NumVerify API."""
    
    name = "number_verify"
    description = "Validating phone numbers and retrieving details such as location, carrier, and line type using NumVerify API."
    args_schema: Optional[Type[BaseModel]] = NumVerifyArgs

    def _run(self, phone_number: str, country_code: Optional[str] = None) -> str:
        # Your NumVerify API key (replace 'YOUR_API_KEY' with your actual API key):
        numverify_api_key = '53ba6969a210072d820b0c14b0492feb'
        # Base URL for NumVerify API
        api_url = f"http://apilayer.net/api/validate?access_key={numverify_api_key}&number={phone_number}"
        
        # Append country_code if provided
        if country_code:
            api_url += f"&country_code={country_code}"

        try:
            # Making an HTTP request to the NumVerify API:
            with urllib.request.urlopen(api_url) as api_response:
                # Parsing the JSON response:
                response_data = json.loads(api_response.read().decode())
                # Checking if the API request was successful
                if response_data.get('valid', False):
                    # Extracting phone number details from the response:
                    country_name = response_data.get('country_name', 'Unknown')
                    location = response_data.get('location', 'Unknown')
                    carrier = response_data.get('carrier', 'Unknown')
                    line_type = response_data.get('line_type', 'Unknown')
                    # Returning the phone number details in a formatted string:
                    return (f"Phone Number: {phone_number}\n"
                            f"Country: {country_name}\n"
                            f"Location: {location}\n"
                            f"Carrier: {carrier}\n"
                            f"Line Type: {line_type}")
                else:
                    # Handling cases where the number is not valid
                    error_message = response_data.get('error', {}).get('info', 'Invalid phone number or unknown error.')
                    return f"Failed to validate phone number. Error: {error_message}"
        except Exception as error_encountered:
            # Returning an error message for any exception that occurs:
            return f"An error occurred while retrieving phone number details: {str(error_encountered)}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    # Creating an instance of the NumVerify and retrieving phone details for a sample number:
    numverify_tool = NumVerify()
    print(numverify_tool._run('+14158586273', 'US'))
