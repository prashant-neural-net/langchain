import os

import streamlit as st
from dotenv import load_dotenv
from langchain.Cache.generate_key import create_cache_key
from langchain.Cache.redis_cache import RedisCache
from langchain_core.prompts import load_prompt
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_openai import ChatOpenAI

cache = RedisCache()
load_dotenv()


llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b", task="text-generation", provider="auto"
)
model_name = "llama3.2:3b"

chat_model = ChatOpenAI(
    model=model_name, base_url=os.environ["Base_Url"], temperature=0
)
model = ChatHuggingFace(llm=llm)

st.header("Research Tool")

paper_input = st.selectbox(
    "Select Research Paper Name",
    [
        "Attention is all you need",
        "BERT: Pre-Training of Deep Bidirectional Transformers",
        "GPT-3: Language Models are Few-Shot Learners",
        "Diffusion Models Beat GANs on Image Synthesis",
    ],
)

style_input = st.selectbox(
    "Select Explanation Style",
    ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"],
)

length_input = st.selectbox(
    "Select Explanation Length",
    ["Short (1-2 paragraphs)", "Medium(3-5 paragraphs)", "Long (detailed explantion)"],
)
template = load_prompt('/home/L/langchain/langchain_prompt/template.json')

if st.button("Summarize"):
    prompt = template.invoke(
        {
            "paper_input": paper_input,
            "style_input": style_input,
            "length_input": length_input,
        }
    )

    prompt_text = prompt.to_string()

    cache_key = create_cache_key(
        prompt_text,
        model_name=model_name,
        temperature=0.0,
    )

    cached_response = cache.get(cache_key)

    if cached_response is not None:
        st.info("Response loaded from Redis cache")
        st.write(cached_response)

    else:
        st.info("Calling the LLM...")

        response = chat_model.invoke(prompt_text)

        cache.set(cache_key=cache_key, response=response.content, model_name=model_name)

        st.write(response.content)


