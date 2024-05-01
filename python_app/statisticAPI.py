import classes

def getTagclassHierarchy():
    ebene = 0
    resultnr = []
    resultname = []
    all_tags = classes.session.query(classes.tagClass_isSubclassof).all()
    tagswithsuperclasses = []
    for i in all_tags:
        tagswithsuperclasses.append(i.tagclassid_a)
    firstclassesquery = classes.session.query(classes.tagClass).filter(classes.tagClass.tagclassid.notin_(tagswithsuperclasses)).first()
    resultnr.append(str(ebene))
    resultname.append(classes.session.query(classes.tagClass).filter(classes.tagClass.tagclassid==firstclassesquery.tagclassid).first().tagclassname+' ('+str(firstclassesquery.tagclassid)+')')

    def subfunction(supertagclassid, ebene):
        nrquery = classes.session.query(classes.tagClass_isSubclassof).filter_by(tagclassid_b=supertagclassid).all()
        if nrquery == []:
            return
        ebene = ebene + 1
        for i in nrquery:
            resultnr.append(str(ebene))
            resultname.append(classes.session.query(classes.tagClass).filter(classes.tagClass.tagclassid == i.tagclassid).first().tagclassname+' ('+str(i.tagclassid)+')')
            subfunction(i.tagclassid, ebene)

    subfunction(firstclassesquery.tagclassid, ebene)

    index = [0]
    oldprefixlen = 0

    for i in range(len(resultnr)):
        prefix = ''
        for j in range(int(resultnr[i])):
            prefix = prefix + ' '

        if oldprefixlen < len(prefix):
            index.append(1)
        if oldprefixlen == len(prefix):
            index[-1] = index[-1]+1
        if oldprefixlen > len(prefix):
            for k in range(oldprefixlen-len(prefix)):
                del index[-1]
            index[-1] = index[-1] + 1

        oldprefixlen = len(prefix)

        outputindex = ''
        for l in index:
            if outputindex != '':
                outputindex = outputindex + '.' + str(l)
            else:
                outputindex = outputindex + str(l-1)

        print(prefix+outputindex+' '+resultname[i])

#getTagclassHierarchy()

def getPopularComments(minlikes):
    from sqlalchemy import func
    query = classes.session.query(func.count(classes.Person_likes_Comment.personid), classes.Person_likes_Comment.commentid).group_by(classes.Person_likes_Comment.commentid).having(func.count(classes.Person_likes_Comment.personid) >= minlikes).all()
    if query == []:
        print(f"Kein Kommentar hat mindestens {str(minlikes)} Likes.")
    commentids = []
    for i in query:
        commentids.append(i.commentid)
    creatorsquery = classes.session.query(classes.Comment).filter(classes.Comment.commentid.in_(commentids)).all()
    creatorids = []
    for i in creatorsquery:
        creatorids.append([i.commentid, i.creator])
    for i in creatorids:
        namequery = classes.session.query(classes.Person).filter_by(personid=i[1]).first()
        print(f"Der Kommentar mit Nr. {str(i[0])} von {namequery.firstname} {namequery.lastname} hat mindestens {str(minlikes)} Likes.")


#getPopularComments(22)

def getCountryMostPosting():
    from sqlalchemy import func, desc
    countdic = {}

    # Comments
    query = classes.session.query(func.count(classes.Comment.commentid), classes.Comment.placeid).group_by(classes.Comment.placeid).order_by(desc(func.count(classes.Comment.commentid))).all()
    for country in query:
        countdic[country[1]] = country[0]

    # Posts
    queryposts = classes.session.query(func.count(classes.Post.postid), classes.Post.placeid).group_by(classes.Post.placeid).order_by(desc(func.count(classes.Post.postid))).all()
    for i in queryposts:
        countdic[i[1]] = countdic[i[1]] + i[0]

    inverse = [(value, key) for key, value in countdic.items()]
    maxcountry = max(inverse)[1]

    countryname = classes.session.query(classes.Place).filter_by(placeid=maxcountry).first().locationname
    print(countryname)

#getCountryMostPosting()
