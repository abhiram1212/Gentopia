# Importing necessary libraries:
from gentopia.tools.basetool import *
# Importing for making HTTP requests:
import urllib.request
# For parsing JSON responses:
import json
from typing import Any, Optional, Type

class WeatherInfoArgs(BaseModel):
    # city: the city for which to get the weather info:
    city: str

class WeatherInfo(BaseTool):
    """A Tool for retrieving weather information using OpenWeatherMap API."""
    
    name = "weather_info"
    description = "Retrieving current weather information for a given city using OpenWeatherMap."
    args_schema: Optional[Type[BaseModel]] = WeatherInfoArgs

    def _run(self, city: str) -> str:
        # Your OpenWeatherMap API key (replace 'YOUR_API_KEY' with your actual API key):
        openweather_api_key = 'd52eafacacfb54484c2b6b20ee7dffea'
        # The URL for the OpenWeatherMap API endpoint to get the current weather:
        api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweather_api_key}&units=metric"
        try:
            # Making an HTTP request to the OpenWeatherMap API:
            with urllib.request.urlopen(api_url) as api_response:
                # Parsing the JSON response:
                response_data = json.loads(api_response.read().decode())
                # Checking if the API request was successful:
                if response_data['cod'] == 200:
                    # Extracting weather information from the response:
                    temperature = response_data['main']['temp']
                    weather_description = response_data['weather'][0]['description']
                    humidity = response_data['main']['humidity']
                    wind_speed = response_data['wind']['speed']
                    # Returning the weather information in a formatted string:
                    return (f"Current weather in {city}:\n"
                            f"Temperature: {temperature}°C\n"
                            f"Weather: {weather_description}\n"
                            f"Humidity: {humidity}%\n"
                            f"Wind Speed: {wind_speed} m/s")
                else:
                    # Handling errors such as city not found:
                    error_message = response_data.get('message', 'No additional error info provided.')
                    return f"Failed to retrieve weather information for {city}. Error: {error_message}"
        except Exception as error_encountered:
            # Returning an error message for any exception that occurs:
            return f"An error occurred while retrieving the weather information: {str(error_encountered)}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    # Creating an instance of the WeatherInfo and retrieving weather for a sample city, e.g., 'London':
    weather_tool = WeatherInfo()
    print(weather_tool._run('London'))
