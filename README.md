# ReAct Agent Visualization

This project implements a ReAct (Reasoning and Acting) agent using the Gemini AI model, with a Streamlit-based user interface for visualization.

## Article Reference

For a detailed explanation of building a ReAct agent from scratch, check out this article:
[Building a ReAct Agent from Scratch: A Beginner's Guide](https://medium.com/@mauryaanoop3/building-a-react-agent-from-scratch-a-beginners-guide-4a7890b0667e)

## Features

- ReAct agent implementation using Gemini AI
- Web search using DuckDuckGo
- Wikipedia search
- Streamlit-based user interface for visualizing the agent's thought process

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/imanoop7/React-Agent-from-Scratch
   cd React-Agent-from-Scratch
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   Create a `.env` file in the project root and add your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Usage

To run the Streamlit app:

```
streamlit run streamlit_app.py
```

This will open a web browser with the ReAct Agent Visualization interface.

## Project Structure

- `react_agent.py`: Contains the ReActAgent class implementation
- `tools.py`: Defines the search tools (DuckDuckGo and Wikipedia)
- `streamlit_app.py`: Streamlit app for the user interface
- `main.py`: Console-based interaction with the ReAct agent

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
