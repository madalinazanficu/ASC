===== Exercitii =====


**Task 0**  - Alocați un vector de elemente ''struct particle'' în următoarele moduri: global, pe stivă și dinamic.
    * Porniți de la ''task01.c'', ''task02.c'' și, respectiv, ''task03.c''.
    * Câte elemente poti fi alocate maxim prin fiecare metodă? Utilizati comanda ''size'' pentru a vedea bss unde se afla stocate variabilele globale.
    * Pentru a creste dimensiunea stack-ului utilizat de sistem puteti folosi ''ulimit -s unlimited''. Pentru vizualizare si verificare a limitelor sistemului puteti incerca ''ulimit -a''.
    * Pentru a face verificarile codului mai rapide, parcurgeti vectorul cu verificarea vitezei din 5M in 5M - nu pentru fiecare valoare in parte. Exercitiul este despre alocare.

**Task 1**  - Alocați dinamic o matrice de elemente ''struct particle'', in mod liniarizat. Populați aleator matricea astfel încât liniile pare să conțină particule care au componentele vitezei pozitive, iar liniile impare să conțină particule care au componentele vitezei negative. Scalați apoi vitezele tuturor particulelor cu 0.5, ignorând structura matricii, prin folosirea unui cast. Introduceti o verificare pentru alocarea dinamica vs. alocarea "clasica" pe linii. Porniti de la ''task1.c''

**Task 2**  - Studiați alinierea variabilelor în C in fisierul  ''task2.c''
    * Afișati adresele variabilelor declarate în schelet. Ce observați despre aceste adrese? Ce legatură există între acestea și dimensiunea tipului?
    * Calculați dimensiunea structurilor a si b din scheletul de program. Afișati dimensiunea acestora folosind ''sizeof''. Explicați cele observate.
    * Studiați exemplul de aliniere manuală la un multiplu de 16 sau 32 bytes. In cazul in care lucrati pe o arhitectura de 32 de biti, explicati rezultatele observate.
    * Studiati efectul optimizarilor de compilator -O2 sau -O3 asupra alinierii datelor. 

**Task 3**  - Determinați dimensiunea cache-urilor L1 și L2 folosindu-vă de metoda prezentată în curs ({{asc:lab4:asc_-_03_-_ierarhia_de_memorie_si_optimizarea_pentru_memorie.pdf | slide-urile 67-77}}). Utilizati variabile char/int8_t pentru acest task.
    * Folosiți makefile-ul pus la dispoziție pentru a genera graficele.
    * Porniti de la ''task3.c''


**Task 4**  - Determinați dimensiunea unei linii de cache folosindu-vă de metoda prezentată în curs ({{asc:lab4:asc_-_03_-_ierarhia_de_memorie_si_optimizarea_pentru_memorie.pdf | slide-urile 67-77}}).
    * Folosiți makefile-ul pus la dispoziție pentru a genera graficele. Utilizati variabile char/int8_t pentru acest task.
    * Porniti de la ''task4.c''
    * Generați grafice pentru mai multe dimensiuni ale vectorului parcurs astfel încât să depășească mărimea cache-ului L1, L2, respectiv, L3.
    * Mecanismele hardware avansate implementate în arhitecturile de procesoare actuale generează comportamente complexe care nu corespund nepărat modelului simplu prezentat în curs. Aceste mecanisme pot chiar masca dimensiunea reală a linei de cache, fiind astfel necesară testarea cu diferite valori ale vectorului parcurs pentru a putea trage o concluzie informată.
    * Studiati si explicati de ce codurile (identice) si makefile-urile (diferite) de la taskurile 3 si 4 duc la graficele obtinute in cadrul laboratorului. 
    * Combinati intr-un singur grafic "relevant" rezultatele prezentate in taskurile 3 si 4.