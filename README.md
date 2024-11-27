# MongoDB Project

MongoDB Project jest projektem zaliczeniowym z przedmiotów:

- Przetwarzanie w chmurach obliczeniowych 24/25Z
- Modelowanie nierelacyjnych baz danych 24/25Z

## Instalacja

Do instalacji projektu wymagane jest następujące oprogramowanie:
- Docker https://docs.docker.com/engine/install/
- git (`apt install git` Debian & Ubuntu lub `dnf install git` RHEL & Oracle Linux)
- cron

Komendy wymagające podwyższonych uprawnień (wykorzystanie konta root, sudo) będą posiadały prefix `# `

### Krok pierwszy, pobranie repozytorium projektu ### 
`$ git clone https://github.com/koloiyolo/mongodb_project.git`

### Krok drugi, uruchomeinie kontenerów docker ###
`$ cd mongodb_project`

`# docker compose up -d`

### Krok trzeci, uruchomeinie potoku CI/CD ###
`$ export PROJECT_PATH="/path/to/mongodb_project"`

Pamiętaj o zmianie ścieżki przykładowej na ścieżkę całkowitą do pliku `cicd.sh`

`# echo "* * * * * root /path/to/your/project/cicd.sh" >> /etc/crontab`

## Wymagania 

### Przetwarzanie w chmurach obliczeniowych
- [x] Aplikacja CRUD z wdrożeniem w chmurze z użyciem potoku CI/CD.
- [x] Uwzględnione aspekty bezpieczeństwa zarówno przy przesyłaniu jak i przechowywaniu danych. (https, szyfrowanie haseł)
- [x] Wdrożenie w postaci maszyny wirtualnej(użycie Terraform/Ansible) lub kontenera Dockera(docker compose)
- [x] Wdrożenie w architekturze mikrousług - min. Dwie komunikujace się ze sobą maszyny wirtualne lub kontenery Dockera.
- [ ] Wdrożenie uzupełnione o testy (jednostkowe, e2e) w ramach protokołu CI/CD


### Modelowanie Nierelacyjnych Baz Danych - projekt
Napisać program symulujący wypożyczalnie video. Program ma operować na dowolnie wybranej bazie
NoSQL. Ma zawierać 3 rodzaje informacji:
- [x] Lista możliwych do wypożyczenia filmów (Tytuł filmu, Gatunek, reżyser, czas trwania, ocena w
skali od 1 do 10, krótki opis filmu, aktorzy, data dodania filmu do kolekcji)
- [x] Lista klientów wypożyczalni ( imię, nazwisko, adres, telefon, data rejestracji)
- [x] Lista wypożyczeń dla danego klienta (Dane klienta, Tytuł filmu, data i godzina wypożyczenia,
data i godzina planowanego zwrotu, data i godzina faktycznego zwrotu)

Każdy klient może wypożyczyć maksymalnie 3 filmy naraz. Film wypożyczany jest na okres 2 dni.
Program umożliwia zalogowanie się jako administrator wypożyczalni i wówczas oferuje następujące
funkcje:
- [x] Wyświetl listę filmów – wyświetla wszystkie dostępne filmy do wypożyczenia (lp, tytuł, gatunek, reżyser, czas trwania). Ponadto możliwe jest wyświetlenie szczegółowych informacji o każdym z filmów (opis, ocena, obsada aktorska). Filmy wypożyczone nie są uwzględniane na liście (lub są oznaczone jako niedostępne). Możliwe jest także sortowanie oraz wyszukiwanie po tytule lub gatunku.
- [x] Wyświetl listę wszystkich wypożyczeń – wyświetla listę wypożyczeń dokonanych przez każdego
klienta w formie (dane klienta ,tytuł filmu, data i godzina wypożyczenia, data i godzina planowanego zwrotu, data i godzina faktycznego zwrotu). Możliwe jest sortowanie po danych klienta, dacie wypożyczenia oraz wyszukiwanie po danych klienta, id_filmu, tytule filmu, dacie wypożyczenia. Możliwe jest także zwrócenie filmu wypożyczonego przez określonego klienta.
- [x] Wypożycz film – po podaniu tytułu filmu i id_klienta lub jego imienia + nazwiska, jeśli dany film
jest dostępny do wypożyczenia i klient nie przekroczył jeszcze limitu wypożyczeń to program zapisuje fakt wypożyczenia (rejestrując datę i godzinę wypożyczenia, obliczając datę planowanego zwrotu)
- [x] Dodaj nowego klienta.
- [x] Usuń klienta.
- [x] Modyfikuj dane klienta – wyświetla listę wszystkich klientów. I umożliwia modyfikacje
wszystkich danych określonego klienta.
- [x] Dodaj nowy film.
- [x] Modyfikuj opis filmu – wyświetla listę wszystkich filmów i umożliwia modyfikacje wszelkich danych dla każdego filmu danych.
- [x] Usuń film.

Ponadto należy przewidzieć opcję rejestracji nowych użytkowników. Wówczas taki użytkownik może
zobaczyć aktualną listę filmów, listę swoich wypożyczeń, dokonać wypożyczenia filmu. 

Zwroty filmów obsługiwane są wyłącznie przez administratora.

Proszę zaimplementować obsługę błędów (np. przy dodawaniu filmu czy należy zwrócić uwagę czy film o takim tytule już istnieje w bazie i wyświetlić stosowny komunikat, nie można usunąć filmu, które jest aktualnie wypożyczony, nie można usunąć klienta jeśli ma on aktywne wypożyczenia itp).

Baza ma posiadać minimum 10 filmów, 5-ciu użytkowników i 4 aktywne wypożyczenia.

Program powinien posiadać graficzny interfejs użytkownika.