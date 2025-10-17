from improving_graph import (
    create_improving_graph,
    compile_workflow,
)
from grouping_graph import create_grouping_graph
import os
from colorama import Style
from tools.rag_database import check_and_update_rag_database
import json
from output.improved import stories as SAMPLE_IMPROVED_USER_STORIES

# Setting API keys
import os

# Get the key from OPENAI_API_KEY file
if os.path.exists("OPENAI_API_KEY"):
    with open("OPENAI_API_KEY", "r") as f:
        OPENAI_API_KEY = f.read().strip()
else:
    # If the file does not exist, check the environment variable
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Set the environment variable
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

LLM_SERVER = "openai"
LLM_MODEL = "gpt-4o-mini-2024-07-18"
ITERATIONS = 100
THREAD_ID = "1234abcd"


# Ensure paths are relative to the script's actual location
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Storing the user stories here, should add something like a cache later
IMPROVED_USER_STORIES = SAMPLE_IMPROVED_USER_STORIES

# Uncomment this line to start from scratch
# IMPROVED_USER_STORIES = []

GROUPED_USER_STORIES = []

print("Checking RAG database...")
# check_and_update_rag_database(chroma_path=CHROMA_PATH, data_path=DATA_PATH)

print("Creating graph and compiling workflow...")
improving_graph = create_improving_graph(server=LLM_SERVER, model=LLM_MODEL)
improving_workflow = compile_workflow(improving_graph)
grouping_graph = create_grouping_graph(server=LLM_SERVER, model=LLM_MODEL)
grouping_workflow = compile_workflow(grouping_graph)
print("Graphs and workflows created.")

if __name__ == "__main__":
    verbose = False
    while True:
        query = input(
            Style.RESET_ALL
            + "=====> Please enter a user story to improve (or EXIT to stop, GROUP to start user stories grouping): "
        )
        print("\n")
        if query.lower() == "exit":
            break
        if query.lower() == "group":
            print("Starting user stories grouping...")
            # print(IMPROVED_USER_STORIES)
            dict_inputs = {
                "user_stories": json.dumps(IMPROVED_USER_STORIES, indent=4),
            }
            config = {
                "configurable": {
                    "thread_id": THREAD_ID + "_grouping",
                    "recursion_limit": ITERATIONS,
                }
            }
            for event in grouping_workflow.stream(
                dict_inputs,
                config,
            ):
                if verbose:
                    print("\nState Dictionary:", event)
                else:
                    print("\n")
            grouped_stories = grouping_workflow.get_state(config).values[
                "grouped_stories"
            ]
            jira_linked_stories = grouping_workflow.get_state(config).values[
                "jira_linked_stories"
            ]
            # print(grouped_stories)
            GROUPED_USER_STORIES = grouped_stories
            # Save the grouped user stories to a file
            GROUPED_USER_STORIES_FILE = os.path.join(
                BASE_DIR, "output", "grouped_user_stories.json"
            )
            with open(GROUPED_USER_STORIES_FILE, "w") as f:
                # Clear the file before writing
                f.truncate(0)
                # Write the updated list of improved user stories to the file
                json.dump(GROUPED_USER_STORIES, f, indent=4)
            # Save the jira linked stories to a file
            JIRA_LINKED_STORIES_FILE = os.path.join(
                BASE_DIR, "output", "jira_linked_stories.json"
            )
            with open(JIRA_LINKED_STORIES_FILE, "w") as f:
                # Clear the file before writing
                f.truncate(0)
                # Write the updated list of improved user stories to the file
                json.dump(jira_linked_stories, f, indent=4)
        else:
            dict_inputs = {
                "original_user_story": query,
                "current_user_story": query,
            }
            config = {
                "configurable": {
                    "thread_id": THREAD_ID,
                    "recursion_limit": ITERATIONS,
                },
            }

            for event in improving_workflow.stream(
                dict_inputs,
                config,
            ):
                if verbose:
                    print("\nState Dictionary:", event)
                else:
                    print("\n")

            improved_stories = improving_workflow.get_state(config).values[
                "user_stories_history"
            ]
            # Update the improved user stories with those that are generated and not already in the list
            for story in improved_stories:
                json_story = json.loads(story.content)
                IMPROVED_USER_STORIES.append(json_story)

            # Save the improved user stories to a file
            IMPROVED_USER_STORIES_PATH = os.path.join(
                BASE_DIR, "output", "improved_user_stories.json"
            )
            with open(IMPROVED_USER_STORIES_PATH, "w") as f:
                # Clear the file before writing
                f.truncate(0)
                # Write the updated list of improved user stories to the file
                json.dump(IMPROVED_USER_STORIES, f, indent=4)
