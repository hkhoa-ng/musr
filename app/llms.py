from langchain_openai import ChatOpenAI


def get_open_ai(temperature=0, model="gpt-4o"):

    llm = ChatOpenAI(
        model=model,
        temperature=temperature,
        top_p=0,
    )
    return llm


def get_open_ai_json(temperature=0, model="gpt-4o"):
    llm = ChatOpenAI(
        model=model,
        temperature=temperature,
        model_kwargs={"response_format": {"type": "json_object"}},
        top_p=0,
    )
    return llm
