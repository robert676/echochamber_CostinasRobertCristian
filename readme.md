# Echo Chamber – Simularea perspectivelor discursive cu modele LLM

## Scopul proiectului

Acest proiect urmareste simularea fenomenului de "echo chamber", in care aceeasi informatie este interpretata diferit in functie de perspectiva ideologica a celui care o analizeaza.

Aplicatia permite introducerea unui text politic sau social si genereaza reactii din partea unor agenti discursivi diferiti, folosind un model lingvistic de mari dimensiuni (LLM).

## Ideea aplicatiei

In mediul online, utilizatorii sunt adesea expusi predominant la opinii similare cu propriile convingeri. Acest fenomen poate conduce la aparitia unor camere de rezonanta informationale (echo chambers), unde aceeasi informatie este interpretata diferit in functie de grupul din care face parte utilizatorul.

Pentru a ilustra acest comportament, aplicatia genereaza raspunsuri din doua perspective distincte:

    anti_sistem
    pro_european

## Tehnologii utilizate

    Python
    Gradio
    Gemini API
    YAML
    JSONL

## Arhitectura solutiei

Aplicatia este alcatuita din urmatoarele componente:

### 1. Corpus local

Fisierul `corpus_sample.jsonl` contine comentarii etichetate manual in functie de orientarea discursiva.

Fiecare inregistrare contine:

    identificatorul comentariului
    categoria discursiva
    textul comentariului
    sursa

### 2. Agenti discursivi

Fisierul `roles.yaml` defineste comportamentul fiecarui agent.

Fiecare agent contine:

    nume
    descriere
    instructiuni de sistem (system prompt)

Aceste instructiuni determina stilul si perspectiva raspunsului generat.

### 3. Regasirea contextului

Pentru fiecare text introdus de utilizator, aplicatia cauta exemple similare in corpus utilizand o metoda simpla de potrivire a cuvintelor.

Comentariile recuperate sunt utilizate ca exemple de context pentru model.

### 4. Generarea raspunsului

Textul introdus, exemplele recuperate si instructiunile agentului sunt trimise catre modelul Gemini.

Modelul genereaza un raspuns compatibil cu perspectiva agentului selectat.

## Moduri de functionare

### Modul Agent

Utilizatorul selecteaza un singur agent discursiv.

Aplicatia genereaza un raspuns din perspectiva acelui agent.

### Modul Comparatie

Aplicatia genereaza simultan raspunsuri pentru ambii agenti.

Acest mod permite observarea diferentelor de interpretare pentru aceeasi informatie.

## Exemple de utilizare

Intrare:

"Guvernul a anuntat o noua crestere a taxelor."

Rezultat:

    agentul anti_sistem ofera o interpretare critica si contestatara;
    agentul pro_european ofera o interpretare moderata si institutionala.

Exemple complete de rulare sunt disponibile in fisierul demo_outputs.md

## Limitari

    corpusul utilizat este redus si construit manual;
    regasirea contextului utilizeaza o metoda simpla bazata pe cuvinte-cheie;
    calitatea raspunsurilor depinde de modelul lingvistic utilizat;
    raspunsurile generate nu reprezinta informatii factuale, ci simulari de perspectiva.



## Concluzii

    Proiectul demonstreaza modul in care modelele lingvistice pot fi utilizate pentru simularea unor perspective discursive diferite asupra aceluiasi eveniment.

    Rezultatele evidentiaza efectul de interpretare selectiva specific fenomenului de echo chamber si arata cum acelasi mesaj poate produce reactii semnificativ diferite in functie de contextul ideologic utilizat.