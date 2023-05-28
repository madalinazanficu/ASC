### Zanficu Madalina - 333CA - Tema 3 ASC

## Decizii de design si implementare
Pentru hashtable am folosit tehnica linear probing in caz de coliziune.
Functia de hash folosita este cea din laboratorul de SD din anul 1,
fiind la randul ei preluata de pe stackoverflow.

Pentru a avea un loadFactor accetabil, am ales urmatoarea abordare:
1. Inainte de fiecare insert verific load-ul hashtable-ului ce presupune
numarul de elemente curent din hashtable + elementele ce urmeaza sa le adaug
raportat la numarul maxim de bucket-uri ale hashtable-ului.

2. Daca acest load factor depasesete threshold-ul maxim de 80%,
atunci o sa fac resize la hashtable.
Pentru a nu face resize-ul dupa "ochi", am ales un alt threshold de 60%, 
astfel numarul maxim de intrari pe care le va avea hashtabelul este calculcat 
astfel incat in acest moment doar 60% din threshold sa fie ocupat.


## Implementare

1. Toate functiile din schelet folosesc functii pentru paralelizarea 
operatiilor pe GPU. 
Atfel, CORE-ul implementarii mele consta si a temei in sine este: 
alocarea memoriei pe device, copierea datelor de pe host pe device, 
apelarea functiilor de pe device si eliberarea memoriei de pe device.
In plus, am folosit si operatii atomice in interiorul functilor executate 
de kernel, cum ar fi: atomicCAS si atomicExch. O sa explic mai jos de ce am 
folosit aceste operatii.

2. **Insert:** am folosit linear probing ca metoda de tratare a coliziunilor
Implementarea functiei de insert executata pe device este urmatoarea:
- se calculeaza hash-ul pentru cheia ce urmeaza sa fie inserata 
si pozitia corespunzatoare in hashtable
- se verifica daca pe aceasta pozitie exista deja o cheie
- daca nu exista am folosit atomicCAS(compare and swap) pentru a insera cheia
si atomicExch pentru a insera valoarea corespunzatoare cheii
- daca exista, atunci se cauta urmatoarea pozitie libera in hashtable si exista 2 cazuri:
    - daca cheia a fost deja introdusa in hashtable, 
    trebuie sa facem update la valoare
    - daca nu a fost introdusa, atunci o inseram pe prima pozitie 
    libera dupa pozitia unde ar fi trebuie sa fie de fapt inserata

3. **Get**: pentru a cauta valorile am tinut cont de 3 scenarii:
- cheia aferenta valorii se gaseste pe pozitia corespunzatoare in hashtable 
(pos calculat in functie de hash si hmax - capacitatea hashtable-ului)
- cheia sa gaseste pe o alta pozitie, la inserare fiind o coliziune
- sau cheia nu exista in hashtable


4. **Reshape**: 
- copiez toate intrarile (key, value) din hashtable-ul vechi in hashtable-ul nou
- eliberez memoria de pe device alocata pentru hashtable-ul vechi
- schimb pointerul catre hashtable-ul vechi cu pointerul catre hashtable-ul nou
- setez noua capacitate a hashtable-ului (hmax)


## Rulare si pareri personale
Timpul de scris cod pentru tema a fost destul de scurt in comparatie 
cu timpul de debug. De ce? 
Tot weekendul inainte de deadline au fost probleme de inrastructura pe 
hpsl, pe moodle, si pe partitia nvidia-gpu iar local chiar daca am NVIDIA,
 _cudaMalloc nu a functionat.
Astfel "m-am chinuit" sa imi testez codul si sa il fac sa mearga.
Am vreo 6 variante de arhive, fiecare doar cu modificari de coding style, 
care toate merg pe nvidia-gpu, dar pe moodle nu, deci imi cer scuze anticipat 
pentru coding style-ul nu tocmai perfect.

In rest, tema a fost interesanta si m-a ajutat sa inteleg concepetele 
de baza ale programarii pe GPU.

Moreover, am testat pe moodle acceasi arhiva de mai multe ori 
(care trece mereu pe nvidia-gpu) 
si am primit rezultate diferite, deci nu stiu ce sa mai zic.
Pentru a nu exista probleme o sa las un link catre un drive cu cateva poze "dovada" 
si rog in caz ca tema mea nu o sa mearga cand o sa dea iar auto-submit pe moodle 
sa fiu contactata pentru a rezolva problema.In aceste conditii cu hpsl si nvidia-coda 
care merg din cand in cand, chiar am dat tot ce am putut.
