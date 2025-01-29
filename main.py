import os
import requests
import json
import argparse
from typing import Iterator
from datetime import datetime
from elevenlabs.client import ElevenLabs
from elevenlabs import save
from pydub import AudioSegment

VOICE_ID = "VpI99zL3jGxzWWyyt1Fi"

question = """
I am wanting to write a Laravel/Livewire application that allows users to create a list of upcoming deliveries.

The users should be able to add a delivery email address, and then edit or delete it - and also re-order the list
and mark them as completed or failed.

When the user clicks on a delivery email address, it should email the user 2nd in line in the list to let them know
their delivery is on the way.  But we need to consider the first and last delivery in the list.

We should also store the delivery 'day' in a database or exportable file so that the owner of the business can
see how the deliveries went.
"""

def get_llm_response(question) -> tuple[str, str]:
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {openrouter_key}",
        },
        data=json.dumps({
            "model": "deepseek/deepseek-r1",
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        })
    )
    api_response = response.json()
    final_answer = api_response["choices"][0]["message"]["content"]
    thought_process = api_response["choices"][0]["message"]["reasoning"]
    return final_answer, thought_process

def convert_to_audio(text, voice) -> Iterator[bytes]:
    client = ElevenLabs(api_key=elevenlabs_key)
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice,
        model_id="eleven_multilingual_v2",
        voice_settings={
            "stability": 0.5,
            "similarity_boost": 0.5,
        },
        output_format="mp3_44100_128",
    )
    return audio

def text_to_speech(text, voice):
    audio_content = []
    paragraphs = text.split("\n")
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    client = ElevenLabs(api_key=elevenlabs_key)

    for index, paragraph in enumerate(paragraphs):
        audio = convert_to_audio(paragraph, voice)
        save(audio, f"thought_process_{index}.mp3")
    for index, paragraph in enumerate(paragraphs):
        audio = AudioSegment.from_mp3(f"thought_process_{index}.mp3")
        audio_content.append(audio)
    combined_audio = AudioSegment.silent(0, 0)
    for audio in audio_content:
        combined_audio += audio

    for index, paragraph in enumerate(paragraphs):
        os.remove(f"thought_process_{index}.mp3")

    return save_final_audio(combined_audio)

def save_final_audio(combined_audio):
    today_string = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"thought_process-{today_string}.mp3"
    combined_audio.export(filename, format="mp3")
    return filename

def main(question: str, voice: str):
    final_answer, thought_process = get_llm_response(question)

    print(final_answer)
    print("#######################")
    print(thought_process)

    filename = text_to_speech(thought_process, voice)

    return filename

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("question", type=str, help="The question to ask the LLM", default="What is the meaning of life?")
    parser.add_argument("--voice", type=str, help="The voice to use", default=VOICE_ID)
    args = parser.parse_args()
    filename = main(args.question, args.voice)
    print(f"Saved to {filename}")
