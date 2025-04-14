# Virtual Search Assistant

A Python-based virtual assistant using OpenAI's API.

## Setup
1. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the assistant:
   ```
   python main.py
   ```

## Features
- Text-based interaction
- Configurable through config.json
- Uses GPT-3.5-turbo by default
- Simple command-line interface

## Configuration
Edit `config.json` to:
- Change the AI model
- Set a custom wake word
- Enable/disable voice features
- Adjust response length
