import json

# Каждая категория должна быть классом!! Генерация классов из JSON!

class Parser:
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

    def getDishPage(self, title): #HOTFIX title=category.title
        category = title.split('.')[0] 
        for c in self.data['category']:
            if c['title'] == category: # BUILD UP DICTIONARY LIKE IN NP
                cat = c
        if not cat:
            return None
        for d in cat['dishes']:
            if d['title'] == title.split('.')[1]:
                dish = d
        if not dish:
            return None
        res = "<b>{0}</b>\n".format(dish['title'])
        for c in dish['products']:
            res += "{0}\n".format(c["title"])
        res += "Цена: {0}\n".format(dish['price'])
        res += "pic img : {0}".format(dish['picture'])
        return res

#must be private
    def getTitles(self, l):
        res = []
        for c in l:
            res.append(c["title"])
        return res
