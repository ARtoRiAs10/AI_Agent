# main.py
import re
from agents import Agent
from memory import MemoryManager
from tools import search_web

from logger import ConversationLogger
from personas import (
    PROPONENT_PERSONA,
    OPPONENT_PERSONA,
    MODERATOR_PERSONA,
    DIRECTOR_PERSONA,
)

# --- 1. SETUP ---

print("--- Initializing System ---")

# Initialize Logger  # <-- ADD THIS
logger = ConversationLogger()

# Initialize Memory
memory = MemoryManager()

# Initialize Tools
available_tools = {
    "search_web": search_web
}

# Initialize Agents
agent_proponent = Agent(name="Dr. Anya Sharma", persona=PROPONENT_PERSONA)
agent_opponent = Agent(name="Kenji Tanaka", persona=OPPONENT_PERSONA)
agent_moderator = Agent(name="Moderator", persona=MODERATOR_PERSONA)
agent_director = Agent(name="Director", persona=DIRECTOR_PERSONA)

# Agent mapping for easy access
agent_map = {
    "Dr. Anya Sharma": agent_proponent,
    "Kenji Tanaka": agent_opponent,
    "Moderator": agent_moderator
}

# --- 2. THE DEBATE LOOP ---

def run_debate():
    topic = "Should the development of artificial general intelligence (AGI) be paused for safety reasons?"
    max_turns = 8

    
    logger.log(f"DEBATE TOPIC: {topic}\n")
    
    print(f"\n--- DEBATE TOPIC: {topic} ---")
    
    # The Moderator starts the debate
    current_speaker_name = "Moderator"
    
    # Introduce the topic
    opening_prompt = [{'role': 'user', 'content': f'Please introduce the debate topic: "{topic}"'}]
    introduction = agent_moderator.speak(opening_prompt)
    print(f"\n{agent_moderator.name}: {introduction}\n")

    
    logger.log_turn(agent_moderator.name, introduction)
    memory.add_to_memory(agent_moderator.name, introduction)

    for turn in range(max_turns):
        print(f"\n--- Turn {turn + 1}/{max_turns} ---")
        
        # a. Director decides who speaks next
        director_prompt = [
            {'role': 'user', 'content': f"Here is the transcript so far:\n{memory.get_full_transcript()}\n\nWho should speak next?"}
        ]
        next_speaker_name = agent_director.speak(director_prompt).strip()
        
        # Basic validation for director's output
        if next_speaker_name not in agent_map:
            print(f"--- DIRECTOR ERROR: Director chose an invalid speaker '{next_speaker_name}'. Defaulting to Proponent. ---")
            next_speaker_name = "Dr. Anya Sharma" # Failsafe
            
        current_agent = agent_map[next_speaker_name]
        print(f"--- Director has chosen: {current_agent.name} ---")

        # b. Retrieve relevant context for the current speaker
        last_few_turns = "\n".join(memory.transcript[-3:]) # Use last 3 turns as query for RAG
        relevant_context = memory.retrieve_relevant_context(last_few_turns)
        
        # c. Agent speaks (with potential tool use)
        # We give the agent the last 5 messages as short-term memory
        short_term_history = [{'role': 'user', 'content': msg} for msg in memory.transcript[-5:]]
        
        final_response = ""
        # Loop to handle tool use. Usually runs once, but can loop if needed.
        for _ in range(3): # Max 3 tool uses per turn to prevent infinite loops
            response = current_agent.speak(short_term_history, relevant_context)
            
            # Check for tool use command
            tool_match = re.search(r"\[USE_TOOL: (search_web\('([^']*)'\))\]", response)

            if tool_match:
                tool_call = tool_match.group(1)
                tool_name, tool_query = tool_call.split("('")
                tool_query = tool_query[:-2] # Clean up query string
                
                print(f"--- {current_agent.name} wants to use a tool: {tool_call} ---")
                
                logger.log_system_message(f"{current_agent.name} is using a tool: {tool_call}")

                tool_result = available_tools[tool_name](tool_query)
                print(f"--- Tool Result: {tool_result} ---")

                
                logger.log_system_message(f"Tool Result: {tool_result}")

                # Add tool result to history for the agent to use
                short_term_history.append({'role': 'user', 'content': response}) # The tool call itself
                short_term_history.append({'role': 'system', 'content': f"TOOL_RESPONSE: {tool_result}"})
                continue # Go back to the agent for a final response
            else:
                final_response = response
                break # No tool used, exit the loop
        
        # d. Record the final response
        print(f"{current_agent.name}: {final_response}\n")

        
        logger.log_turn(current_agent.name, final_response) 
        memory.add_to_memory(current_agent.name, final_response)
        
        # e. Optional: Moderator summary every 3 turns
        if (turn + 1) % 3 == 0 and turn < max_turns -1:
            print("--- Moderator is summarizing... ---")
            summary_prompt = [{'role': 'user', 'content': 'Please provide a brief, neutral summary of the last few points made by both sides.'}]
            summary = agent_moderator.speak(summary_prompt, context=memory.get_full_transcript())
            print(f"Moderator: {summary}\n")
            
            logger.log_turn("Moderator", summary)
            memory.add_to_memory("Moderator", summary)


    print("--- The Debate Has Concluded! ---")
    
    logger.log("--- The Debate Has Concluded! ---") 
    memory.save_transcript_to_file(topic=topic, file_format='md')

if __name__ == "__main__":
    run_debate()