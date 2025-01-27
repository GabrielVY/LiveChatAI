
import asyncio
import base64
import io
import os
import sys
import traceback
import qasync

import cv2
import pyaudio
import PIL.Image
import mss

import argparse

from google import genai
from google.genai import types
from google.genai.types import HarmCategory, HarmBlockThreshold

if sys.version_info < (3, 11, 0):
    import taskgroup, exceptiongroup

    asyncio.TaskGroup = taskgroup.TaskGroup
    asyncio.ExceptionGroup = exceptiongroup.ExceptionGroup

from dotenv import load_dotenv
load_dotenv()

# COMPILER
import ast

# GUI
from gui.chat_overlay import ChatOverlay
from PyQt5.QtWidgets import QApplication
import random
from datetime import datetime


# TOOLS
FUNCTION_SCHEMA = {
    "tools": [{
        "function_declarations": [{
            "name": "sendChatMessage",
            "description": "Send a user message to a chat.",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "message": {"type": "string"}
                },
                "required": ["username", "message"]
            }
        }]
    }]
}


# PROPERTIES
MODEL_ID = "gemini-2.0-flash-exp"
DEFAULT_MODE = "screen"
REQUEST_TIME = 5 # How long does it take to send a chat request to the AI (Seconds)
TEMPERATURE = 0.5


# USAGE PROMPT
USAGE_PROMPT = """
USAGE:
LIVE CHAT SIMULATOR PROMPT
Only use sendChatMessage(username, message). Never use other functions.

React to gameplay, streamer commentary etc...

Keep messages short, some can be longer if they're good

Send 1-3 messages at a time. Avoid spam.

Vary usernames but keep recurring chatters consistent

Adjust message frequency based on hype (e.g., big moments = more messages)

If no notable events, send no messages

Maintain natural chat behavior with varied reactions.

Do not send the same thing over and over again.

You will be sent a message with the current timestamp each x seconds, after that use the functions to react to the stream.

Try to answer the streamer if they ask anything.

Make sense of what you're seeing, it can get boring if everything is unrelated.

Be attentive to details and subtleties

When sending a message containing \' send instead \\'
\n
CHAT CHARACTER:\n"""

# PROMPT
DEFAULT_PROMPT = """Simulate chaotic Twitch chat reactions. Use sarcastic, meme-heavy humor with Gen Z slang. 
Throw in clueless jokes, rhetorical questions, and light trolling.""".replace("\n", "")


# AUDIO
FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024

pya = pyaudio.PyAudio()


# API
class ChatAPI:

    def __init__(self, overlay):
        self.overlay = overlay

    def sendChatMessage(self, username, message):
        """Send a user message to a chat.

        Args:
            username: The username of the sender.
            message: The content of the chat message to be sent.

        Returns:
            A dictionary containing the message details and delivery status.
        """

        # Schedule the message with a random delay
        asyncio.create_task(self._send_with_delay(username, message))

        return {
            "username": username,
            "message": message,
            "status": "success",
            "timestamp": datetime.now().isoformat(timespec='seconds')
        }
    
    async def _send_with_delay(self, username, message):
        """Internal helper to send a message after a random delay."""
        delay = random.uniform(0, REQUEST_TIME)  # Random delay between 0 and REQUEST_TIME seconds
        await asyncio.sleep(delay) # Simulate the delay
        self.overlay.add_message(username, message)  # Send the message
    

class LiveFeed:

    def __init__(self, overlay, gemini_key=None, prompt=DEFAULT_PROMPT, video_mode=DEFAULT_MODE, voice_recording=True, safety_system=True):
        if not gemini_key:
            gemini_key = os.getenv("GEMINI_API_KEY")

        self.client = genai.Client(api_key=gemini_key, http_options={'api_version': 'v1alpha'})
        self.session = None
        self.chat_api = ChatAPI(overlay)

        self.voice_recording = voice_recording
        self.audio_in_queue = None
        self.audio_stream = None

        # Send out the frames
        self.out_queue = None
        self.video_mode = video_mode

        # AI
        self.prompt = USAGE_PROMPT + prompt

        # Safety system
        safety_level = HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
        if not safety_system:
            safety_level = HarmBlockThreshold.BLOCK_NONE

        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: safety_level,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: safety_level,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: safety_level,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: safety_level,
            HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY: HarmBlockThreshold.BLOCK_NONE
        },

        # CONFIG
        self.config = {
                "generation_config": {
                    "response_modalities": ["TEXT"],
                    "temperature": TEMPERATURE,
                    "max_output_tokens": 100,
                    "top_p": 0.9,
                    "top_k": 40,
                },
            "system_instruction": self.prompt,
            "safety_settings": safety_settings,
            **FUNCTION_SCHEMA
        }

        self.shutdown_event = asyncio.Event()
    
    # Trigger the AI to send messages back (By using ChatAPI)
    async def trigger_comments(self):
        #msg = "Send!"
        msg = datetime.now().isoformat(timespec='seconds')
        while not self.shutdown_event.is_set():
            print(f"[DEBUG] Triggering comment at {datetime.now().isoformat()}")
            await asyncio.sleep(REQUEST_TIME)  # Every REQUEST_TIME seconds
            msg = datetime.now().isoformat(timespec='seconds')
            await self.session.send(input=[msg], end_of_turn=True)

    # Execute the functions contained within the response
    async def execute_functions(self, content):
        model_turn = content.model_turn
        
        if not model_turn:
            return

        for part in model_turn.parts:
            executable_code = part.executable_code
            if executable_code is not None:
                try:
                    tree = ast.parse(executable_code.code)
                    code_object = compile(tree, '<string>', 'exec')
                    #print(executable_code)
                    exec(code_object, {'default_api': self.chat_api, 'sendChatMessage': self.chat_api.sendChatMessage})
                except Exception as e:
                    print(f"Error executing code: {e}")
                    traceback.print_exc()

            #code_execution_result = part.code_execution_result
            #if code_execution_result is not None:
            #    print(f"B: {code_execution_result}")

        return

    # Capture your audio in real time
    async def listen_audio(self):
        mic_info = pya.get_default_input_device_info()
        self.audio_stream = await asyncio.to_thread(
            pya.open,
            format=FORMAT,
            channels=CHANNELS,
            rate=SEND_SAMPLE_RATE,
            input=True,
            input_device_index=mic_info["index"],
            frames_per_buffer=CHUNK_SIZE,
        )
        if __debug__:
            kwargs = {"exception_on_overflow": False}
        else:
            kwargs = {}
        while not self.shutdown_event.is_set():
            data = await asyncio.to_thread(self.audio_stream.read, CHUNK_SIZE, **kwargs)
            await self.out_queue.put({"data": data, "mime_type": "audio/pcm"})
    
    # Send back function response
    async def handle_tool_call(self, tool_call):
        for fc in tool_call.function_calls:
            tool_response = types.LiveClientToolResponse(
                function_responses=[types.FunctionResponse(
                    name=fc.name,
                    id=fc.id,
                    response={'result':'ok'},
                )]
            )

        #print('\n>>> ', tool_response)
        await self.session.send(input=tool_response)
    
    # Handle each AI response
    async def handle_responses(self):
        while not self.shutdown_event.is_set():
            async for response in self.session.receive():

                server_content = response.server_content

                if server_content is not None:
                    await self.execute_functions(server_content)

                tool_call = response.tool_call
                if tool_call is not None:
                    await self.handle_tool_call(tool_call)

    # Screen capture
    def _get_screen(self):
        sct = mss.mss()
        monitor = sct.monitors[0]

        i = sct.grab(monitor)

        mime_type = "image/jpeg"
        image_bytes = mss.tools.to_png(i.rgb, i.size)
        img = PIL.Image.open(io.BytesIO(image_bytes))

        image_io = io.BytesIO()
        img.save(image_io, format="jpeg")
        image_io.seek(0)

        image_bytes = image_io.read()
        return {"mime_type": mime_type, "data": base64.b64encode(image_bytes).decode()}
    
    # Screen capture loop (Put each frame at the end of out_queue)
    async def get_screen(self):
        while not self.shutdown_event.is_set():
            frame = await asyncio.to_thread(self._get_screen)
            if frame is None:
                break
            
            # Update frames each 1 second
            await asyncio.sleep(1.0)

            await self.out_queue.put(frame)

    # Send video feed
    async def send_realtime(self):
        while not self.shutdown_event.is_set():
            msg = await self.out_queue.get()
            await self.session.send(input=msg)

    # Main loop
    async def run(self):
        try:
            async with (
                self.client.aio.live.connect(model=MODEL_ID, config=self.config) as session,
                asyncio.TaskGroup() as tg,
            ):
                self.session = session

                # Initialize queue
                self.audio_in_queue = asyncio.Queue()
                self.out_queue = asyncio.Queue(maxsize=5)

                print("Connected to Gemini API")

                # Send video feed
                tg.create_task(self.send_realtime())

                # Record your audio
                if self.voice_recording:
                    tg.create_task(self.listen_audio())

                if self.video_mode == "camera":
                    pass
                    #tg.create_task(self.get_frames())
                elif self.video_mode == "screen":
                    tg.create_task(self.get_screen())

                # Trigger comments and receive API messages
                tg.create_task(self.trigger_comments())
                tg.create_task(self.handle_responses())

                await self.shutdown_event.wait()  # Wait until shutdown event is set
        except asyncio.CancelledError:
            pass
        except ExceptionGroup as EG:
            #self.audio_stream.close()
            traceback.print_exception(EG)
        finally:
            if self.audio_stream:
                self.audio_stream.close()
            self.session = None
            print("Disconnected...")

    def stop(self):
        """Signal the shutdown event and close resources."""
        self.shutdown_event.set()

        if self.audio_stream:
            self.audio_stream.close()
