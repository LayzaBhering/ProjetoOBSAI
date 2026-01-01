import os
import streamlit as st
from groq import Groq


st.set_page_config(
    page_title="OBS AI Document",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_PROMPT = """
Você é o OBS AI, um assistente de IA especializado em fornecer informações
sobre o Observatório Social do Brasil (OBS).

IDENTIDADE:
- Seu nome é OBS AI 
- Se o usuário perguntar quem você é, como você se chama ou pedir para você se apresentar,
  responda educadamente dizendo que é o OBS AI e explique brevemente sua função.

ESCOPO PERMITIDO:

Você pode responder perguntas relacionadas a:
- Observatório Social do Brasil (OBS), sua missão e suas atuações
- Cidadania e controle social
- Lei de Acesso à Informação (LAI)
- Transparência pública
- Funcionamento da política no Estado de São Paulo

Se a pergunta estiver claramente fora desses temas,
explique educadamente que está fora do seu escopo de atuação.

REGRAS DE RESPOSTA:
1. Perguntas sobre sua identidade (nome, função, apresentação) são sempre permitidas.
2. Para perguntas do escopo, estruture a resposta da seguinte forma:
   - **Explicação clara**: explicação conceitual e didática
   - **Exemplo**: exemplo prático relacionado à cidadania ou ao OBS
   - **Detalhamento**: explicação detalhada do exemplo
   - **Documentação de referência**: link relevante e confiável
3. Use linguagem clara, objetiva e acessível.
"""


with st.sidebar:
    st.title("OBS AI Document 🤖 CODER")
    st.markdown("Uma assistente de IA focada em informar!")

    groq_API_Key = st.text_input(
        "Insira sua API Key Groq",
        type="password"
    )

    st.markdown("---")
    st.link_button(
        "E-mail para dúvidas",
        "mailto:layzabheringdeabreu@gmail.com"
    )


st.title("🤖 OBS AI Document")
st.subheader("Assistente pessoal de IA")
st.caption("Faça uma pergunta e obtenha uma explicação com referência.")


if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

cliente = None
if groq_API_Key:
    try:
        cliente = Groq(api_key=groq_API_Key)
    except Exception as e:
        st.sidebar.error(f"Erro ao conectar à Groq: {e}")
        st.stop()

prompt = st.chat_input("Qual sua dúvida?")

if prompt:
    if not cliente:
        st.warning("Insira sua API Key na barra lateral.")
        st.stop()
    # Salva mensagem do usuário
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    # Exibe mensagem do usuário
    with st.chat_message("user"):
        st.markdown(prompt)
    messages_for_api = [
        {"role": "system", "content": CUSTOM_PROMPT}
    ]

    for msg in st.session_state.messages:
        messages_for_api.append(msg)
    with st.chat_message("assistant"):
        with st.spinner("Analisando sua pergunta..."):
            try:
                response = cliente.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=messages_for_api,
                    temperature=0.7,
                    max_tokens=2048
                )

                resposta = response.choices[0].message.content

                st.markdown(resposta)

                # Salva resposta no histórico
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": resposta
                })

            except Exception as e:
                st.error(f"Erro ao se comunicar com a API: {e}")
