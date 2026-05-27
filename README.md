# Kreator Scenariuszy Testowych AI

Aplikacja webowa zbudowana w Streamlit, która pozwala tworzyć i uruchamiać automatyczne scenariusze testowe dla aplikacji webowych przy użyciu agenta AI sterowanego przeglądarką.

## Opis

Narzędzie jest przeznaczone dla testerów, którzy chcą zautomatyzować manualne scenariusze testowe bez pisania kodu. Użytkownik definiuje kolejne kroki testu w formularzu, a agent AI wykonuje je w przeglądarce, a następnie generuje raport z przebiegu testu w formacie Markdown.

## Wymagania

- Python 3.10 lub nowszy
- Klucz API do modelu Gemini (Google AI)
- Przeglądarka obsługiwana przez `browser-use`

Zależności Pythona:

```
streamlit
browser-use
python-dotenv
```

Zainstaluj je poleceniem:

```bash
pip install streamlit browser-use python-dotenv
```

## Konfiguracja

Utwórz plik `.env` w katalogu głównym projektu i umieść w nim swój klucz API:

```
GOOGLE_API_KEY=twoj_klucz_api
```

## Uruchomienie

```bash
streamlit run app.py
```

Aplikacja domyślnie uruchamia się pod adresem `http://localhost:8501`.

## Użytkowanie

1. Podaj adres URL aplikacji, którą chcesz przetestować.
2. Wypełnij kroki scenariusza testowego. Domyślnie załadowanych jest kilka przykładowych kroków dotyczących listy zakupów.
3. Dodawaj lub usuwaj kroki za pomocą przycisków pod formularzem.
4. W panelu po prawej stronie możesz podejrzeć prompt, który zostanie wysłany do agenta.
5. Kliknij przycisk "URUCHOM AUTOMATYCZNY TEST", aby rozpocząć wykonywanie scenariusza.
6. Po zakończeniu agent wygeneruje raport z testem zawierający podsumowanie kroków, obserwacje i werdykt.

## Uwagi

Agent posiada wbudowane opóźnienie 5 sekund pomiędzy kolejnymi akcjami, aby uniknąć przekroczenia limitów zapytań do API. Czas wykonywania testu zależy od liczby kroków i złożoności testowanej aplikacji.

Raport generowany przez agenta zawiera:

- podsumowanie wykonanych kroków,
- obserwacje dotyczące zachowania aplikacji,
- ostateczny werdykt testu.

## Struktura projektu

```
.
├── app.py          # Główny plik aplikacji
├── .env            # Plik z kluczami API (nie commitować do repozytorium)
└── README.md
```