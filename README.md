# Live Chat Simulation via Gemini API

This project simulates a live chat that interacts with the Gemini API. It dynamically responds to your activity by sending screen frames and voice recordings to the API. A chat window displays messages to the user based on the interaction.

**Warning**: Using the Gemini API may incur charges depending on your usage and the API's billing policy. Ensure you review the [Gemini API pricing details](https://ai.google.dev/pricing) before proceeding. By using this software, you accept responsibility for any costs incurred.

## Features

- **Real-Time Screen Sharing**: Continuously captures and sends screen frames to the Gemini API.
- **Voice Interaction**: Records audio and sends it as part of the communication.
- **Interactive Chat**: Displays a live chat interface that shows responses from the Gemini API.

---

## Prerequisites

Before you get started, ensure you have the following:

- Python 3.11.0 or higher installed on your system
- A Gemini API key
- Required Python dependencies (listed in `requirements.txt`)

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/GabrielVY/LiveChatAI
   cd LiveChatAI
   ```

2. **Set Up the Environment: Create a .env file in the root of the project and add your Gemini API key:**
   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```
   
3. **Install Dependencies: Install the required Python libraries using the following command:**
   ```bash
   pip install -r requirements.txt
   ```
   
## Usage

1. **Run the Program: Execute the main program using:**
   ```bash
   python main_gui.py
   ```

2. **How It Works:**
  - The program captures your screen frames in real-time.
  - It records your voice input.
  - The captured data is sent to the Gemini API.
  - Responses from the Gemini API are displayed in the chat window.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
