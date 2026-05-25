import asyncio
from dotenv import load_dotenv

from browser_use import Agent, ChatGoogle

load_dotenv()

async def main():
    llm = ChatGoogle(
        model="gemini-3.1-flash-lite", 
        temperature=0.0
    )

    task_description = """
    Jesteś testerem manualnym. Testujesz aplikację na http://localhost:5173/.
    
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
       - Ostateczny werdykt (np. "TEST ZALICZONY").
    """

    agent = Agent(
        task=task_description,
        llm=llm,
    )

    original_step = agent.step
    
    async def rate_limited_step(*args, **kwargs):
        print("\n⏳ Hamulec anty-limitowy: Czekam 5 sekund przed kolejną akcją...")
        await asyncio.sleep(5)
        return await original_step(*args, **kwargs)
        
    agent.step = rate_limited_step

    print("Uruchamiam agenta Gemini... (Otworzy się okno przeglądarki)")
    result = await agent.run()
    
    print("\n=========================================")
    print("           RAPORT Z TESTU                ")
    print("=========================================\n")
    
    final_report = result.final_result()
    
    if final_report:
        print(final_report)
    else:
        print("Agent zakończył pracę, ale nie wygenerował poprawnego raportu tekstowego.")

if __name__ == "__main__":
    asyncio.run(main())