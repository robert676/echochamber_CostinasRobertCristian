import os
import json
import yaml
import gradio as gr

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def load_corpus():
    corpus = []

    with open("data/corpus_sample.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line:
                corpus.append(json.loads(line))

    return corpus


def load_roles():
    with open("roles.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["agents"]


CORPUS = load_corpus()
ROLES = load_roles()


def retrieve_context(input_text, agent_slug, k=3):

    input_words = set(input_text.lower().split())

    results = []

    for item in CORPUS:

        if item["agent"] != agent_slug:
            continue

        text_words = set(item["text"].lower().split())

        score = len(input_words & text_words)

        results.append(
            {
                "text": item["text"],
                "score": score,
                "source": item["source"]
            }
        )

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:k]


def build_prompt(input_text, contexts):

    retrieved_text = "\n".join(
        [f"- {item['text']}" for item in contexts]
    )

    prompt = f"""
[TEXT DE COMENTAT]

{input_text}

[EXEMPLE SIMILARE DIN CORPUS]

{retrieved_text}

[SARCINA]

Scrie un comentariu scurt ca reactie la TEXTUL DE COMENTAT.
Exemplele similare sunt doar inspiratie de ton si stil.
Nu copia exemplele.
Nu inventa fapte noi.
Raspunde in maximum 3 propozitii.
"""

    return prompt


def call_llm(system_prompt, user_prompt):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Lipseste GEMINI_API_KEY. Creeaza fisierul .env din .env.example."

    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    response = client.chat.completions.create(
        model=os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash-lite"
        ),
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return response.choices[0].message.content


def generate_agent_response(agent_slug, input_text):

    role = ROLES[agent_slug]

    contexts = retrieve_context(
        input_text,
        agent_slug
    )

    prompt = build_prompt(
        input_text,
        contexts
    )

    return call_llm(
        role["system"],
        prompt
    )


def compare_agents(input_text):

    anti = generate_agent_response(
        "anti_sistem",
        input_text
    )

    pro = generate_agent_response(
        "pro_european",
        input_text
    )

    return anti, pro


with gr.Blocks() as demo:

    gr.Markdown("# EchoChamber")

    with gr.Tab("Agent"):

        txt = gr.Textbox(
            label="Text de analizat"
        )

        agent = gr.Dropdown(
            choices=[
                "anti_sistem",
                "pro_european"
            ],
            value="anti_sistem",
            label="Agent"
        )

        out = gr.Textbox(
            label="Raspuns"
        )

        btn = gr.Button("Genereaza")

        btn.click(
            generate_agent_response,
            inputs=[agent, txt],
            outputs=out
        )

    with gr.Tab("Comparatie"):

        txt_compare = gr.Textbox(
            label="Text de analizat"
        )

        compare_btn = gr.Button("Compara")

        anti_out = gr.Textbox(
            label="Anti-sistem"
        )

        pro_out = gr.Textbox(
            label="Pro-european"
        )

        compare_btn.click(
            compare_agents,
            inputs=txt_compare,
            outputs=[
                anti_out,
                pro_out
            ]
        )

demo.launch()