import classes

def getProfile(pid):
    persquery = classes.session.query(classes.Person).filter_by(personid=int(pid))
    print('Person ' + str(persquery.first().firstname)+' ' + str(persquery.first().lastname) + ':')
    print('Geburtstag: '+str(persquery.first().birthday))
    print('Geschlecht: ' + str(persquery.first().gender))
    if persquery.first().studyorganisation == []:
        print('Studienorganisation: kein Universitätsbesuch')
    else:
        for i in persquery.first().studyorganisation:
            print('Studienorganisation: ' + str(i.name))
    if persquery.first().workorganisation == []:
        print('Arbeitgeber: keiner')
    else:
        for i in persquery.first().workorganisation:
            print('Arbeitgeber: ' + str(i.name))
    cityquery = classes.session.query(classes.City).filter_by(placeid=persquery.first().placeid)
    countryquery = classes.session.query(classes.Country).filter_by(placeid=cityquery.first().ispartof) # originally instead of .filter_by -> .join(classes.City, tr.City.ispartof==tr.Country.placeid).filter(classes.City.placeid == persquery.first().placeid)
    continentquery = classes.session.query(classes.Continent).filter_by(placeid=countryquery.first().ispartof)
    print('Wohnort: ' + str(cityquery.first().name) + ', ' + str(countryquery.first().name) + ', ' + str(continentquery.first().name))

#Testing:
#getProfile(12094627905604)
    #12094627905604

def getCommonInterestsOfMyFriends(pid):
    persontags = classes.session.query(classes.Person_hasinterest).filter_by(personid=pid).all()
    taglist = []
    for tag in persontags:
        taglist.append(tag.tagid)
    query = classes.session.query(classes.Person_hasinterest).join(classes.pkp_symmetric, classes.pkp_symmetrickp_symmetric.personid_b==classes.Person_hasinterest.personid_a).filter(classes.Person_hasinterest.tagid.in_(taglist), classes.pkp_symmetric.personid_a == pid)

    results = query.all()
    for row in results:
        print(f"Friend ID: {row.personid}, Tag ID: {row.tagid}")


# Testing:
#getCommonInterestsOfMyFriends(8796093022217)

def getCommonFriends(pid, fid):
    fidfriends = classes.session.query(classes.pkp_symmetric).filter_by(personid=fid).all()
    friendslist = []
    for friend in fidfriends:
        friendslist.append(friend.personid_b)
    query = classes.session.query(classes.pkp_symmetric).filter(classes.pkp_symmetric.personid_a == pid, classes.pkp_symmetric.personid_b.in_(friendslist))
    results = query.all()
    for row in results:
        nameofperson = classes.session.query(classes.Person).filter_by(personid=row.personid_b).first()
        print(f"Die Person {row.personid_b} ({nameofperson.firstname} {nameofperson.lastname}) ist gemeinsamer Freund von {pid} und {fid}.")
#Testing:
#getCommonFriends(8796093022217,3298534883405)

def getPersonsWithMostCommonInterests(pid):
    from sqlalchemy import func, desc
    from sqlalchemy.orm import aliased
    pe = aliased(classes.Person_hasinterest)
    pz = aliased(classes.Person_hasinterest)
    query = classes.session.query(func.count(pz.tagid), pz.personid).join(pe, pe.tagid == pz.tagid).group_by(pz.personid).filter(pe.personid == pid).order_by(desc(func.count(pz.tagid)))
    if len(query.all()) <= 1:
        print('Die eingegebene Person hat keine geteilten Interessen.')
    else:
        mostid = list(query.all()[1])[1]
        nameofperson = classes.session.query(classes.Person).filter_by(personid=mostid).first()
        print(f"Die Person {mostid} ({nameofperson.firstname} {nameofperson.lastname}) hat die meisten geteilten Interessen mit {pid}.")

#Testing:
#getPersonsWithMostCommonInterests(12094627905604)

def getJobRecommendation(pid): # Firma finden anhand von Uni
    query = classes.session.query(classes.Person).filter_by(personid=pid).first()
    currentplaces = []
    if query.studyorganisation == []:
        print('Die eingegebene Person hat keine Uni besucht.')
    else:
        for i in query.studyorganisation:
            currentplaces.append(i.placeid)
    if query.workorganisation == []:
        print('Die Person hat keine Arbeitsstellen gehabt.')
    else:
        for i in query.workorganisation:
            currentplaces.append(i.placeid)
    if currentplaces == []:
        print('Die Person hat bisher keine Studien- oder Arbeitsorte gehabt, weshalb keine Empfehlung gegeben werden kann.')
        return None
    friendquery = classes.session.query(classes.pkp_symmetric).filter_by(personid_a=pid).all()
    friendlist = []
    if friendquery == []:
        print('Die Person hat keine Freunde, weshalb keine Empfehlung gegeben werden kann.')
        return None
    else:
        for i in friendquery:
            friendlist.append(i.personid_b)
    orgquery = classes.session.query(classes.Organisation).filter(classes.Organisation.placeid.in_(currentplaces)).all()
    possibleorgs = []
    if orgquery == []:
        print('An den bisherigen Studien- und Arbeitsorten der Person gibt es keine Firma oder Uni, weshalb keine Empfehlung gegeben werden kann.')
        return None
    else:
        for i in orgquery:
            possibleorgs.append(i.organisationid)
    orgsoffriend = []
    friendinfoquery = classes.session.query(classes.Person).filter(classes.Person.personid.in_(friendlist)).all()
    for person in friendinfoquery:
        orgs = person.workorganisation
        if orgs != []:
            for i in orgs:
                orgsoffriend.append(i.organisationid)
        unis = person.studyorganisation
        if unis != []:
            for i in unis:
                orgsoffriend.append(i.organisationid)
    if orgsoffriend == []:
        print('Von den Freunden arbeitet oder studiert niemand, weshalb keine Empfehlung gegeben werden kann.')
        return None
    finalquery = classes.session.query(classes.Organisation).filter(classes.Organisation.organisationid.in_(possibleorgs), classes.Organisation.organisationid.in_(orgsoffriend)).all()
    if finalquery == []:
        print('Es konnte keine Uni oder Firma an einem der Arbeits- oder Studienorte der eingegebenen Person gefunden werden, an der ein Freund der eingegebenen Person arbeitet.')
        return None
    else:
        for i in finalquery:
            print(f"Die Organisation {i.name} wird der eingegebenen Person empfohlen.")

#12094627905604 -> keine Freunde
#3298534883405
#getJobRecommendation(2199023255633)

def getShortestFriendshipPath(pid, fid, visited=None): #no auto-print!
    if visited is None:
        print(f"Der schnellste Weg von {pid} zu {fid} führt über folgenden Weg:")
        visited = set()  # Create a set to store visited person IDs

    visited.add(pid)  # Mark the starting person as visited
    print(visited)

    pidfriendsquery = classes.session.query(classes.pkp_symmetric).filter_by(personid_a=pid).all()
    for friend in pidfriendsquery:
        if friend.personid_b == fid:
            return f"{fid}"  # Found a direct friend (shortest path)
        elif friend.personid_b not in visited:  # Only explore unvisited friends
            path = getShortestFriendshipPath(friend.personid_b, fid, visited.copy())
            if path:
                return f"{friend.personid_b}-{path}"  # Prepend current friend to path
    return None  # No path found

#Testing: 8796093022217
#print(getShortestFriendshipPath(2199023255633, 3298534883405))
#print(getShortestFriendshipPath(2199023255633, 8796093022217))
#print(getShortestFriendshipPath(3298534883405, 12094627905604)) # ?