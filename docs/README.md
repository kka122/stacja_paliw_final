# Symulator stacji benzynowej

## Opis projektu
To prosty symulator stacji benzynowej napisany w Pythonie. Umożliwia:

Obsługę klientów tankujących paliwo,

Wydawanie paliwa (benzyna, diesel itp.),

Zapisywanie historii transakcji,

Obliczanie średniej ceny paliwa na podstawie sprzedaży,

Podstawową symulację stanów magazynowych.

Projekt może służyć jako podstawa do nauki programowania obiektowego oraz operacji na plikach w Pythonie.
## Struktura katalogów
symulator_stacji/
│
├── main.py                  # Główny plik uruchamiający symulację
├── stacja.py                # Logika działania stacji (klasy, metody)
├── paliwo.py                # Klasy reprezentujące różne typy paliw
├── transakcje.py            # Rejestracja i historia transakcji
├── magazyn.py               # Obsługa magazynu i stanów paliwa
├── utils.py                 # Funkcje pomocnicze (np. formatowanie, walidacja)
│
├── data/
│   ├── historia.json        # Zapis historii transakcji (JSON)
│   └── magazyn.json         # Dane o stanie magazynu
│
├── tests/
│   ├── test_stacja.py       # Testy jednostkowe dla klasy stacji
│   └── test_paliwo.py       # Testy jednostkowe dla paliwa
│
├── README.md                # Dokumentacja projektu
└── requirements.txt         # Lista zależności (jeśli używane)
## przyszle ulepszenia

Interfejs użytkownika (GUI lub webowy)

Logowanie pracowników i autoryzacja

Wiele stanowisk tankowania

Dodanie fakturowania i paragonów

