# MongoDB Project #

MongoDB Project jest projektem zaliczeniowym z przedmiotów:

- Przetwarzanie w chmurach obliczeniowych 24/25Z
- Modelowanie nierelacyjnych baz danych 24/25Z

## Instalacja ##

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
