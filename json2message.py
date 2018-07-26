import json


# Каждая категория должна быть классом!! Генерация классов из JSON!


class Json2Message:
    def __init__(self, query):
        self.data = json.loads(query)

    # TODO : make it more abstractive
    def getDishesList(self, cat):
        for c in self.data["category"]:
            if c["title"] == cat:
                category = c
        if not category:
            return None
        return self.getTitles(category['dishes'])

    def getCategoriesList(self):
        return self.getTitles(self.data['category'])

    def getDishPage(self, title):  # HOTFIX title=category.title
        category = title.split('.')[0]
        for c in self.data['category']:
            if c['title'] == category:  # BUILD UP DICTIONARY LIKE IN NP
                cat = c
        if not cat:
            return None
        for d in cat['dishes']:
            if d['title'] == title.split('.')[1]:
                dish = d
        if not dish:
            return None
        res = {}
        res['title'] = dish['title']
        composition = ""
        for c in dish['products']:
            composition += "{0}\n".format(c["title"])
        res['composition'] = composition
        res['price'] = dish['price']
        res['pic'] = dish['picture']
        return res

    # must be private
    def getTitles(self, l):
        res = []
        for c in l:
            res.append(c["title"])
        return res
