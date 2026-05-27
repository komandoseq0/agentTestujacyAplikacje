import asyncio
import streamlit as st
from dotenv import load_dotenv
from browser_use import Agent, ChatGoogle

load_dotenv()

st.set_page_config(page_title="Formularz Testera AI", layout="wide")

if 'num_steps' not in st.session_state:
    st.session_state.num_steps = 6
    st.session_state.step_0 = "Dodaj do listy zakupów 4 jabłka z odpowiednią kategorią."
    st.session_state.step_1 = "Dodaj do listy zakupów ser gouda 40g z odpowiednią kategorią."
    st.session_state.step_2 = "Zmień w przeglądaniu listy wyświetlania kategorię na ser."
    st.session_state.step_3 = "Zmień w przeglądaniu listy wyświetlania kategorię na owoce."
    st.session_state.step_4 = "Usuń jabłka."
    st.session_state.step_5 = "Zmień w przeglądaniu listy wyświetlania kategorię na all."

async def run_agent(task_description):
    llm = ChatGoogle(
        model="gemini-3.1-flash-lite", 
        temperature=0.0
    )

    agent = Agent(
        task=task_description,
        llm=llm,
    )

    original_step = agent.step
    
    async def rate_limited_step(*args, **kwargs):
        st.toast("Hamulec anty-limitowy: Czekam 5 sekund przed kolejną akcją...")
        await asyncio.sleep(5)
        return await original_step(*args, **kwargs)
        
    agent.step = rate_limited_step

    result = await agent.run()
    return result.final_result()


st.title("Kreator Scenariuszy Testowych AI")
st.markdown("Wypełnij poniższy formularz, aby dostosować test i uruchomić Agenta AI.")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("1. Konfiguracja ogólna")
    app_url = st.text_input("Adres URL testowanej aplikacji:", value="http://localhost:5173/")

    st.subheader("2. Kroki scenariusza testowego")
    st.markdown("Edytuj lub dodaj akcje, które agent ma wykonać krok po kroku:")
    
    for i in range(st.session_state.num_steps):
        st.text_input(f"Krok {i+1}:", key=f"step_{i}")

    btn_col1, btn_col2 = st.columns([1, 1])
    with btn_col1:
        if st.button("Dodaj kolejny krok", use_container_width=True):
            st.session_state.num_steps += 1
            st.session_state[f"step_{st.session_state.num_steps-1}"] = ""
            st.rerun()
            
    with btn_col2:
        if st.button("Usuń ostatni krok", use_container_width=True) and st.session_state.num_steps > 0:
            if f"step_{st.session_state.num_steps-1}" in st.session_state:
                del st.session_state[f"step_{st.session_state.num_steps-1}"]
            st.session_state.num_steps -= 1
            st.rerun()

skonstruowane_kroki = []
for i in range(st.session_state.num_steps):
    krok_tekst = st.session_state.get(f"step_{i}", "")
    if krok_tekst.strip():
        skonstruowane_kroki.append(krok_tekst)

task_description = f"""Jesteś testerem manualnym. Testujesz aplikację na {app_url}.

Kroki do wykonania dokładnie w tej kolejności:
1. Wejdź na {app_url}.
"""

for idx, step in enumerate(skonstruowane_kroki):
    task_description += f"{idx+2}. {step}\n"

numer_zakonczenia = len(skonstruowane_kroki) + 2
task_description += f"""{numer_zakonczenia}. GŁÓWNA ZASADA ZAKOŃCZENIA: Kiedy wykonasz wszystkie powyższe kroki, MUSISZ użyć akcji 'done', aby natychmiast zakończyć pracę i zapobiec powtarzaniu kroków! 
W parametrze tej akcji napisz profesjonalny, czytelny raport z testu w formacie Markdown. Raport ma zawierać:
   - Krótkie podsumowanie wykonanych kroków.
   - Obserwację końcową (np. czy po wpisaniu zmyślonych danych aplikacja poprawnie pokazała błąd).
   - Ostateczny werdykt (np. "TEST ZALICZONY")."""


with col2:
    st.subheader("Jak to widzi AI?")
    st.caption("Poniższe pole generuje się automatycznie na podstawie formularza po lewej i zostanie wysłane do Agenta.")
    st.text_area("Podgląd promptu systemowego:", value=task_description, height=450, disabled=True)

st.divider()

if st.button("URUCHOM AUTOMATYCZNY TEST", type="primary", use_container_width=True):
    if not app_url:
        st.error("Wprowadź adres URL aplikacji przed uruchomieniem testu!")
    elif len(skonstruowane_kroki) == 0:
        st.error("Dodaj przynajmniej jeden krok do scenariusza testowego!")
    else:
        with st.spinner("Trwa testowanie... Agent analizuje stronę i wykonuje Twoje kroki z formularza. Proszę czekać."):
            try:
                final_report = asyncio.run(run_agent(task_description))
                
                st.success("Scenariusz testowy został wykonany!")
                st.divider()
                
                st.subheader("Wynik i Raport z Testu")
                if final_report:
                    st.markdown(final_report)
                else:
                    st.error("Agent zakończył pracę, ale nie wygenerował poprawnego raportu tekstowego.")
                    
            except Exception as e:
                st.error(f"Wystąpił błąd podczas działania agenta: {e}")