import asyncio
import streamlit as st
from dotenv import load_dotenv
from browser_use import Agent, ChatGoogle

load_dotenv()

st.set_page_config(page_title="Tester AI", page_icon="🤖", layout="wide")

DEFAULT_PROMPT = """Jesteś testerem manualnym. Testujesz aplikację na http://localhost:5173/.

Kroki do wykonania dokładnie w tej kolejności:
1. Wejdź na http://localhost:5173/.
2. Dodaj do listy zakupów 4 jabłka z odpowiednią kategorią.
3. Dodaj do listy zakupów ser gouda 40g z odpowiednią kategorią.
4. Zmień w przeglądaniu listy wyświetlania kategorię na ser.
4. Zmień w przeglądaniu listy wyświetlania kategorię na owoce.
6. Usuń jabłka.
7. Zmień w przeglądaniu listy wyświetlania kategorię na all.
8. GŁÓWNA ZASADA ZAKOŃCZENIA: Kiedy wykonasz wszystkie powyższe kroki, MUSISZ użyć akcji 'done', aby natychmiast zakończyć pracę i zapobiec powtarzaniu kroków! 
W parametrze tej akcji napisz profesjonalny, czytelny raport z testu w formacie Markdown. Raport ma zawierać:
   - Krótkie podsumowanie wykonanych kroków.
   - Obserwację końcową (np. czy po wpisaniu zmyślonych danych aplikacja poprawnie pokazała błąd).
   - Ostateczny werdykt (np. "TEST ZALICZONY")."""

async def run_agent(task_description):
    """Funkcja asynchroniczna uruchamiająca agenta z przekazanym promptem."""
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
        st.toast("Hamulec anty-limitowy: Czekam 5 sekund przed kolejną akcją...", icon="⏳")
        await asyncio.sleep(5)
        return await original_step(*args, **kwargs)
        
    agent.step = rate_limited_step

    result = await agent.run()
    return result.final_result()


st.title("Asystent - Tester Aplikacji Webowych")
st.markdown("Witaj! Możesz tu edytować scenariusz testowy i zlecić jego wykonanie agentowi AI.")

user_prompt = st.text_area(
    "Instrukcje dla testera (możesz je dowolnie zmieniać):", 
    value=DEFAULT_PROMPT, 
    height=350
)

if st.button("Uruchom Test", type="primary", use_container_width=True):
    
    with st.spinner("Trwa testowanie... Agent analizuje stronę. Proszę czekać, niebawem otworzy się przeglądarka."):
        try:
            final_report = asyncio.run(run_agent(user_prompt))
            
            st.success("Test zakończony pomyślnie!")
            st.divider()
            
            # Wyświetlanie raportu
            st.subheader("Raport z testu")
            if final_report:
                st.markdown(final_report)
            else:
                st.error("Agent zakończył pracę, ale nie wygenerował poprawnego raportu tekstowego.")
                
        except Exception as e:
            st.error(f"Wystąpił błąd podczas działania agenta: {e}")