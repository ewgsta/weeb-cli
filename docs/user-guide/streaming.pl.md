# Streamowanie anime

Dowiedz się, jak streamować anime bezpośrednio w odtwarzaczu multimedialnym.

## Rozpoczynanie streamu

### Z wyników wyszukiwania

1. Wyszukaj anime
2. Wybierz anime z wyników
3. Wybierz opcję "Oglądaj"
4. Wybierz odcinek
5. Wybierz jakość/serwer
6. Wideo otwiera się w odtwarzaczu MPV

### Z listy obserwowanych

1. Menu główne → Lista obserwowanych
2. Wybierz anime
3. Wybierz odcinek
4. Stream się rozpoczyna

## Sterowanie odtwarzaczem

### Skróty klawiszowe MPV

- Spacja: Odtwórz/Wstrzymaj
- Strzałka w lewo/prawo: Przewiń do tyłu/do przodu o 5 sekund
- Strzałka w górę/dół: Przewiń do tyłu/do przodu o 1 minutę
- [ / ]: Zmniejsz/Zwiększ prędkość odtwarzania
- m: Wycisz/Włącz dźwięk
- f: Przełącz pełny ekran
- q: Zamknij odtwarzacz
- s: Zrób zrzut ekranu
- j: Przełączaj napisy

### Śledzenie postępu

Weeb CLI automatycznie:
- Zapisuje Twoją pozycję co 15 sekund
- Oznacza odcinek jako obejrzany przy 80% ukończenia
- Synchronizuje postęp z trackerami (jeśli skonfigurowano)

### Wznów oglądanie

Gdy ponownie otworzysz odcinek:
- Automatycznie wznawia od ostatniej pozycji
- Pokazuje monit o wznowienie, jeśli blisko końca
- Czyści pozycję po ukończeniu

## Wybór jakości

### Dostępne jakości

Zależy od dostawcy i serwera:
- 1080p (Full HD)
- 720p (HD)
- 480p (SD)
- 360p (Niska)
- Auto (adaptacyjna)

### Wybieranie jakości

1. Po wybraniu odcinka
2. Wybierz spośród dostępnych jakości
3. Wyższa jakość wymaga szybszego połączenia

### Problemy z jakością

Jeśli buforuje:
1. Wybierz niższą jakość
2. Sprawdź prędkość internetu
3. Spróbuj innego serwera

## Wybór serwera

### Wiele serwerów

Większość dostawców oferuje wiele serwerów:
- Serwer główny (zwykle najszybszy)
- Serwery zapasowe
- Różne usługi hostingowe

### Przełączanie serwerów

Jeśli stream zawiedzie:
1. Wróć do wyboru odcinka
2. Spróbuj innego serwera
3. Różne serwery mogą mieć różne jakości

## Napisy

### Obsługa napisów

- Wbudowane napisy (jeśli dostępne)
- Zewnętrzne pliki napisów
- Obsługa wielu języków

### Sterowanie napisami

W MPV:
- j: Przełączaj ścieżki napisów
- v: Przełącz widoczność napisów
- z/x: Dostosuj opóźnienie napisów

## Problemy ze streamowaniem

### Wideo się nie odtwarza

1. Sprawdź instalację MPV
2. Spróbuj innej jakości/serwera
3. Sprawdź połączenie internetowe
4. Sprawdź, czy URL streamu jest prawidłowy

### Buforowanie

1. Obniż ustawienie jakości
2. Wstrzymaj i pozwól na buforowanie
3. Sprawdź prędkość sieci
4. Spróbuj innego serwera

### Synchronizacja audio/wideo

1. Użyj klawiszy z/x do dostosowania
2. Spróbuj innego serwera
3. Zgłoś problem, jeśli się utrzymuje

### Brak napisów

1. Sprawdź, czy dostawca oferuje napisy
2. Spróbuj innego serwera
3. Użyj klawisza j, aby przełączać ścieżki napisów

## Zaawansowane funkcje

### Discord Rich Presence

Jeśli włączone, pokazuje na Discord:
- Obecnie oglądane anime
- Numer odcinka
- Upłynięty czas

Włącz w: Ustawienia → Integracje → Discord RPC

### Statystyki oglądania

Zobacz swoje statystyki:
- Całkowity czas oglądania
- Obejrzane odcinki
- Ulubione anime
- Historia oglądania

Dostęp: Menu główne → Lista obserwowanych → Statystyki

## Wskazówki

1. Użyj pełnego ekranu (klawisz f) dla najlepszego doświadczenia
2. Dostosuj prędkość odtwarzania klawiszami [ ]
3. Rób zrzuty ekranu klawiszem s
4. Używaj klawiszy strzałek do szybkiego przewijania
5. Włącz Discord RPC, aby dzielić się z przyjaciółmi

## Następne kroki

- [Przewodnik pobierania](downloading.md): Pobierz do oglądania offline
- [Integracja trackerów](trackers.md): Synchronizuj swój postęp
- [Lokalna biblioteka](library.md): Zarządzaj pobranymi anime
