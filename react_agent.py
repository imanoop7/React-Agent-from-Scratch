import json
import time
from typing import List, Dict, Any
from google.api_core import exceptions as google_exceptions

class ReActAgent:
    def __init__(self, model):
        self.model = model
        self.tools: Dict[str, Any] = {}
        self.messages: List[Dict[str, str]] = []
        self.max_iterations = 5

    def register_tool(self, name: str, func: callable):
        self.tools[name] = func

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def get_chat_history(self):
        return "\n".join([f"{m['role']}: {m['content']}" for m in self.messages])

    def run(self, query: str, max_retries=3, retry_delay=1):
        self.add_message("user", query)
        
        for iteration in range(self.max_iterations):
            prompt = self.create_prompt(query)
            print(f"Iteration {iteration + 1}: Sending prompt to model")
            
            for attempt in range(max_retries):
                try:
                    response = self.model.generate_content(prompt)
                    response_text = response.text
                    print(f"Model response: {response_text}")
                    break
                except google_exceptions.GoogleAPIError as e:
                    print(f"API Error on attempt {attempt + 1}: {str(e)}")
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(retry_delay)
            
            try:
                parsed_response = json.loads(response_text)
                print(f"Parsed response: {parsed_response}")
                
                if "action" in parsed_response:
                    print("Processing action")
                    self.process_action(parsed_response)
                elif "answer" in parsed_response:
                    print("Processing answer")
                    return self.process_answer(parsed_response)
                else:
                    print("Invalid response format")
                    self.add_message("system", "Error: Invalid response format")
            
            except json.JSONDecodeError:
                print("Failed to parse response as JSON")
                self.add_message("system", "Error: Failed to parse response as JSON")
        
        print("Max iterations reached without finding an answer")
        return "I apologize, but I couldn't find a satisfactory answer within the given number of iterations."

    def create_prompt(self, query: str):
        return f"""You are a ReAct (Reasoning and Acting) agent. Your goal is to answer the user's query by reasoning about the problem and using available tools when necessary.

Query: {query}

Previous reasoning and observations:
{self.get_chat_history()}

Available tools: {', '.join(self.tools.keys())}

Respond in the following JSON format:

If you need to use a tool:
{{
    "thought": "Your reasoning about what to do next",
    "action": {{
        "tool": "Name of the tool to use",
        "input": "Input for the tool"
    }}
}}

If you have enough information to answer the query:
{{
    "thought": "Your final reasoning process",
    "answer": "Your comprehensive answer to the query"
}}

Remember to be thorough in your reasoning and use tools when you need more information."""

    def process_action(self, parsed_response):
        thought = parsed_response["thought"]
        action = parsed_response["action"]
        self.add_message("assistant", f"Thought: {thought}")
        
        tool_name = action["tool"]
        tool_input = action["input"]
        
        if tool_name in self.tools:
            tool_result = self.tools[tool_name](tool_input)
            self.add_message("system", f"Observation: {tool_result}")
        else:
            self.add_message("system", f"Error: Tool '{tool_name}' not found")

    def process_answer(self, parsed_response):
        thought = parsed_response["thought"]
        answer = parsed_response["answer"]
        self.add_message("assistant", f"Thought: {thought}")
        self.add_message("assistant", f"Final Answer: {answer}")
        return answer
