from data import menu

def search_menu(query):
    query = query.strip().lower()
    if query == "":
        return menu
    results = []
    for item in menu:
        if query in item["name"].lower() or query in item["category"].lower():
           results.append(item) 
    return results

