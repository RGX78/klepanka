import re
import json
from collections import Counter

# Wczytaj tekst z pliku (zakladajac ze uzytkownik podal ksiazke jako tekst)
# Dla testu uzyjemy przykladowego tekstu z Insomnia
text = """No one – least of all Dr Litchfield – came right out and told
Ralph Roberts that his wife was going to die, but there came a
time when Ralph understood without needing to be told. The
months between March and June were a jangling, screaming
time inside his head – a time of conferences with doctors, of
evening runs to the hospital with Carolyn, of trips to other
hospitals in other states for special tests (Ralph spent much of
his travel time on these trips thanking God for Carolyn's Blue
Cross/Major Medical coverage), of personal research in the
Derry Public Library, at first looking for answers the specialists
might have overlooked, later on just looking for hope and
grasping at straws.
Those four months were like being dragged drunk through
some malign carnival where the people on the rides were really
screaming, the people lost in the mirror maze were really lost,
and the denizens of Freak Alley looked at you with false smiles
on their lips and terror in their eyes. Ralph began to see these
things by the middle of May, and as June set in, he began to
understand that the pitchmen along the medical midway had
only quack remedies to sell, and the cheery quickstep of the
calliope could no longer quite hide the fact that the tune spilling
out of the loudspeakers was 'The Funeral March'. It was a
carnival, all right; the carnival of lost souls.
Ralph continued to deny these terrible images – and the even
more terrible idea lurking behind them – all through the early
summer of 1992, but as June gave way to July, this finally
became impossible. The worst midsummer heatwave since 1971
rolled over central Maine, and Derry simmered in a bath of
hazy sun, humidity, and daily temperatures in the mid-nineties.
The city – hardly a bustling metropolis at the best of times –
fell into a complete stupor, and it was in this hot silence that
Ralph Roberts first heard the ticking of the deathwatch and
understood that in the passage from June's cool damp greens
to the baked stillness of July, Carolyn's slim chances had
become no chances at all. She was going to die. Not this
summer, probably – the doctors claimed to have quite a few
tricks up their sleeves yet, and Ralph was sure they did – but
this fall or this winter. His longtime companion, the only woman
he had ever loved, was going to die. He tried to deny the idea,
scolding himself for being a morbid old fool, but in the gasping
silences of those long hot days, Ralph heard that ticking
everywhere – it even seemed to be in the walls.
Yet it was loudest from within Carolyn herself, and when she
turned her calm white face toward him – perhaps to ask him
to turn on the radio so she could listen while she shelled some
beans for their supper, or to ask him if he would go across to
the Red Apple and get her an ice-cream on a stick – he would
see that she heard it, too. He would see it in her dark eyes, at
first only when she was straight, but later even when her eyes
were hazed by the pain medication she took. By then the
ticking had grown very loud, and when Ralph lay in bed beside
her on those hot summer nights when even a single sheet
seemed to weigh ten pounds and he believed every dog in
Derry was barking at the moon, he listened to it, to the
deathwatch ticking inside Carolyn, and it seemed to him that his
heart would break with sorrow and terror. How much would
she be required to suffer before the end came? How much
would he be required to suffer? And how could he possibly live
without her?"""

STOP_WORDS = set("""the be to of and a in that have i it for not on with he as you do at this but his by from they we say her she or an will my one all would there their what so up out if about who get which go me when make can like time no just him know take people into year your good some could them see other than then now look only come its over think also back after use two how our work first well way even new want because any these give day most us was are had been has were said did done does am is being having shall should may might must need dare ought used let every own old very still here where down right left more much many same too before great little something anything nothing everything away again off long while such upon without through been being doing having going""".split())

# Usun znaki specjalne, podziel na slowa
words = re.findall(r"[a-z]+(?:['-][a-z]+)*", text.lower())

# Filtruj: tylko slowa >= 4 znaki, nie stop words, czestotliwosc >= 2
freq = Counter(w for w in words if len(w) >= 4 and w not in STOP_WORDS)

# Wybierz trudne slowa (rzadkie - wystepujace 2-5 razy)
# lub po prostu posortowane po czestotliwosci
sorted_words = sorted(freq.items(), key=lambda x: x[1])

# Wez top 150 trudnych slow (najrzadszych, ale >= 2 wystapien)
uncommon = [w for w, c in sorted_words if 2 <= c <= 5][:150]

print(f"Znaleziono {len(uncommon)} trudnych slow:")
print(json.dumps(uncommon, indent=2, ensure_ascii=False))
