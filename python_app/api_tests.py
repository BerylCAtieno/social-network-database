import classes

def getCommonInterestsOfMyFriends(pid):
    persontags = classes.session.query(classes.Person_hasinterest).filter_by(personid=pid).all()
    taglist = []
    for tag in persontags:
        taglist.append(tag.tagid)
    query = classes.session.query(classes.Person_hasinterest).join(classes.pkp_symmetric, classes.pkp_symmetrickp_symmetric.personid_b==classes.Person_hasinterest.personid_a).filter(classes.Person_hasinterest.tagid.in_(taglist), classes.pkp_symmetric.personid_a == pid)

    results = query.all()
    for row in results:
        print(f"Friend ID: {row.personid}, Tag ID: {row.tagid}")

getCommonInterestsOfMyFriends(8796093022217)