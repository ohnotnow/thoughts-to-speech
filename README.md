# Thoughts to Speech

A Python application that leverages an LLM (via OpenRouter) to generate 'thinking' responses to user questions, then converts the response into speech using ElevenLabs.

## Repository

[GitHub Repository](https://github.com/ohnotnow/thoughts-to-speech)

## Features

- Uses OpenRouter to generate AI responses to text queries.
- Converts text responses into speech using ElevenLabs.
- Outputs the generated speech as an MP3 file.

## Installation

Ensure you have Python installed (>= 3.8). Then, clone the repository and install dependencies:

```sh
# Clone the repository
git clone https://github.com/ohnotnow/thoughts-to-speech.git
cd thoughts-to-speech

# Install dependencies
uv sync
```

> `uv` is a modern Python package manager. Learn more at [uv documentation](https://docs.astral.sh/uv/).

## Environment Variables

Before running the application, set up the required API keys as environment variables:

```sh
export OPENROUTER_API_KEY="your_openrouter_api_key"
export ELEVENLABS_API_KEY="your_elevenlabs_api_key"
```

On Windows (PowerShell):

```powershell
$env:OPENROUTER_API_KEY="your_openrouter_api_key"
$env:ELEVENLABS_API_KEY="your_elevenlabs_api_key"
```

## Usage

Run the script with a question and an optional voice ID:

```sh
uv run main.py "I have x, y and z to do today, what should I do first?"
```

You can also specify a custom voice:

```sh
uv run main.py "I have an old app running Laravel 5.8, how do I upgrade it to Laravel 11?" --voice "your_elevenlabsvoice_id"
```

Or you can run the script without a question and it will prompt you for one:

```sh
uv run main.py
```

## Output

The program prints the AI-generated response and reasoning, then saves the synthesized speech as an MP3 file:

```
Saved to thought_process-YYYY-MM-DD-HH-MM-SS.mp3
```

## License

This project is licensed under the MIT License.
