# Maxipes-Fik

Proč tento nástroj existuje?
Když v Blenderu zrcadlíš nebo škáluješ objekt do mínusových hodnot a zapomeneš aplikovat transformace, Blender ho sice ve 3D okně vykresluje správně, ale pro herní engine se model matematicky "převrátí naruby". Unreal Engine používá z důvodu optimalizace výkonu techniku Backface Culling (záměrně nevykresluje zadní strany polygonů). Výsledkem je pak rozbitý, z poloviny průhledný mesh, skrz který jde vidět.

Inspektor Fík tě zachrání před zdlouhavým detektivním hledáním těchto chyb přímo v Unrealu a vyřeší problém na jedno kliknutí ještě před samotným exportem.

Hlavní funkce
Okamžitá detekce: Skript bleskurychle projde celou scénu a najde všechny polygonální meshe, které mají negativní měřítko (Scale na ose X, Y nebo Z menší než 0).

Automatický výběr: Všechny problémové objekty se rovnou označí, abys je mohl okamžitě hromadně opravit.

Vlastní UI v N-Panelu: Přidává dedikovanou záložku s přehledným rozhraním přímo do pracovního prostoru.

Vizuální zpětná vazba:

Chyba: Pokud najde rozbitý objekt, zobrazí varování, návod k opravě a příslušnou ikonu Fíka.

Čistý stav: Pokud je scéna připravená na export, Fík tě odmění spokojeným vizuálem.

Instalace
Stáhni si tento repozitář jako .zip soubor (obsahuje __init__.py a zdrojové obrázky).

V Blenderu v horním menu otevři Edit > Preferences.

V levém sloupci vyber Add-ons.

Klikni na tlačítko Install... (nebo v Blenderu 4.2+ na šipku a Install from Disk) a vyber stažený .zip soubor.

Zaškrtni prázdné políčko vedle názvu Object: MaxipesFik pro aktivaci nástroje.

Jak Fíka používat
Ve 3D Viewportu stiskni klávesu N pro otevření pravého bočního panelu.

Najdi a rozklikni záložku Inspektor Fík.

Stiskni tlačítko Vypustit Fíka!

Pokud nástroj najde rozbité objekty, vybere je. Následně stiskni Ctrl + A a zvol Scale. Tím Blenderu řekneš, že nová velikost je výchozí stav, a normály se srovnají.

Můžeš Fíka vypustit znovu pro kontrolu, že je vše čisté.
<img width="597" height="418" alt="maxipes_fik" src="https://github.com/user-attachments/assets/e3a65b78-5bc2-4ae1-a894-e6165de08771" />
