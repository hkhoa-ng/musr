# Instruction for running the Docker container

- Clone this repository.
- Setup the documents necessary for the RAG model to run. Gather your related project & company documentations as PDF files, and put them under `/app/data/` folder. For this example, I've generated a set imaginary company documents under `/app/data/`. You can use those, or replace them with yours.
- Install Docker on your machine: [Install Docker Engine](https://docs.docker.com/engine/install/).
- Ensure that you can use Docker by running: `docker run -d -p 8080:80 docker/welcome-to-docker` and visit [http://localhost:8080](http://localhost:8080) in your browser.
- In the root directory of the cloned repo, run `docker build -t mas-app .`. This command will build the application into a container.
- To run this app, you need an OpenAI's API key. Get yours at [OpenAI's project page](https://platform.openai.com/settings/organization/api-keys). The API key should come in the format of `sk-...`.
- After building, the Docker container can be run with `docker run -it -e OPENAI_API_KEY="<your API key>" mas-app`, for example `docker run -it -e OPENAI_API_KEY="sk-proj-ABCD" mas-app`. This will run the application in interaction mode, and you can interact with the command shell. After this, just follow the prompt to use the application. I've also created some draft user stories to use as inputs for the system, under the `/sample_us/` folder. Just pick a user story in there and copy to the system's prompt.
- In any case that you want access to your artefacts e.g., the output user story files of this app, you can use the command `docker run -it --rm -e OPENAI_API_KEY="<your API key>" mas-app /bin/bash` to run the `bash` shell of the Docker container. Here, you can use `cd` and `cat` to navigate the file system, and get the content of the output files. They should be at `/src/app/output/`, named as `improved_user_stories.json` and `grouped_user_stories.json`.
- Every time you update the project documents under `/app/data/`, remember to build the app again with `docker build -t mas-app .`. This will update the ChromaDB's artefacts and the RAG model will able to use your new documentations.
- In the `/app/output/improved.py`, you can include the improved user stories for later runs. Right now, it's possible that the tool runs into a recursion limit after 4-5 user stories, so it might not be possible to run through a large patch of user stories in 1 run. You can copy the improved user stories from the `/src/app/output/improved_user_stories.json` (using the method mentioned above) into the `/app/output/improved.py` folder. Then, the tool can use those stories in the grouping and linking tasks. If you want to start from scratch everytime, and ignore the stories in `/app/output/improved.py`, go to the `/app/main.py`, and uncomment the line of code on line 54.

# Instruction for using the tool

- After running the app in interactive mode with `docker run -it -e OPENAI_API_KEY="<your API key>" mas-app`, follow the prompt on screen to use the app. The first prompt will be to input an original user story for improvement, or typing `GROUP` to start user story grouping & linking, or `EXIT` to stop the process. For improvement workflow, just copy your original user story as raw text, and hit enter to start the process.
- The agent will start working, and the results from their responses will be printed on screen in different colors for ease of tracking. At the end, you will be prompted with an immediate user story, and the agents will ask for your feedback and approval of the improvement.
- You can provide your feedback for their results. **Please be as direct as possible**, e.g., acceptance criteria #3 is not needed, review other ACs too, since the agents can't understand abstract feedback very well. If you have feedback and feel like the quality is not good enough yet, provide your feedback through the CLI and give `false` as your approval, e.g., `> Human: do the results pass your final approval (true/false)? false`
- The process is repeated, and you will be presented with another user story, modified based on your feedback. Again, provide your feedback, and if it looks good, give `true` as your approval this time, e.g., `> Human: do the results pass your final approval (true/false)? true`
- The story will be saved in the `/src/app/output/improved_user_stories.json` file, and the tool will ask you to provide another user story, or to continue to the grouping stage. Rinse and repeat as many time as we want, then use `GROUP` to continue to the next stage
- The grouping stage is similar to the improving stage. The agents will do their work, and ask for your feedback at the end. Again, provide your feedback, give your approval (`true` or `false`), similar to the improving stage. The results will be saved in the `/src/app/output/grouped_user_stories.json` and `/src/app/output/jira_linked_stories.json`

# About data

- All the data provided for the RAG should be provided in PDF format, and put into the `/app/data/` directory. I've put some samples in there from our university project
- The system's output is in the `/app/output/` folder
- I have some sample original user stories from the project, and those are inside `/app/sample_us/`, feel free to use them to get familiar with the tool, before using your own dataset
