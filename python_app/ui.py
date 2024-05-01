import sys

print("Das Programm bietet folgende Funktionen:")
print("1. Profil einer Person ausgeben")
print("2. gemeinsame Interessen einer Person mit deren Freunden ausgeben")
print("3. gemeinsame Freunde zweier Personen ausgeben")
print("4. zu einer Person die Person mit den meisten geteilten Interessen ausgeben")
print("5. zu einer Person eine Jobempfehlung abgeben")
print("6. den kürzesten Weg zwischen zwei Personen über Freundschaftsbeziehungen ausgeben")
print("7. Hierarchie der Tag-Klassen anzeigen")
print("8. Kommentare mit einer eingegebenen Mindest-Like-Anzahl ausgeben")
print("9. Land mit den meisten Postings und Kommentaren anzeigen")
print("")
funcnr = 0
while funcnr not in range(1,10):
    print("Zur Auswahl einer Funktionalität bitte eine Zahl zwischen 1 und 9 angeben:")
    funcnr = int(input())

if funcnr == 1:
    print("Gib bitte die ID der Person ein, von der das Profil ausgegeben werden soll:")
    pid = int(input())
    from PersonRelatedAPI import getProfile
    getProfile(pid)

if funcnr == 2:
    print("Gib bitte die ID der Person ein, deren gemeinsame Interessen mit ihren Freunden ausgegeben werden soll:")
    pid = int(input())
    from PersonRelatedAPI import getCommonInterestsOfMyFriends
    getCommonInterestsOfMyFriends(pid)

if funcnr == 3:
    print("Zur Ausgabe der gemeinsamen Freunde bitte eine der beiden abzufragenden Person-IDs eingeben:")
    pid = int(input())
    print("Zur Ausgabe der gemeinsamen Freunde bitte die andere der beiden abzufragenden Person-IDs eingeben:")
    fid = int(input())
    from PersonRelatedAPI import getCommonFriends
    getCommonFriends(pid, fid)

if funcnr == 4:
    print("Bitte die ID der abzufragenden Person eingeben:")
    pid = int(input())
    from PersonRelatedAPI import getPersonsWithMostCommonInterests
    getPersonsWithMostCommonInterests(pid)

if funcnr == 5:
    print("Bitte die ID der Person, für die eine Jobempfehlung ausgesprochen werden soll, eingeben:")
    pid = int(input())
    from PersonRelatedAPI import getJobRecommendation
    getJobRecommendation(pid)

if funcnr == 6:
    print("Zur Anzeige des kürzesten Pfades über Freundesbeziehungen die ID der ersten der beiden Personen angeben:")
    pid = int(input())
    print("Zur Anzeige des kürzesten Pfades über Freundesbeziehungen die ID der anderen Person angeben:")
    fid = int(input())
    from PersonRelatedAPI import getShortestFriendshipPath
    print(getShortestFriendshipPath(pid, fid))

if funcnr == 7:
    from statisticAPI import getTagClassHierarchy
    getTagClassHierarchy()

if funcnr == 8:
    print("Wie viele Likes sollen die auszugebenden Kommentare mindestens haben?")
    minlikes = int(input())
    from statisticAPI import getPopularComments
    getPopularComments(minlikes)

if funcnr == 9:
    from statisticAPI import getCountryMostPosting
    getCountryMostPosting()