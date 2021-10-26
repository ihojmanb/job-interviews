import json
import requests

credentials = open("credentials.json")
credentials = json.load(credentials)
api_key = credentials["api-key"]
# print(api_key)

url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&query=pasta"
res = requests.get(url).json()
results = res["results"][0]
id = results["id"]
print(results)
print(id)


class Recipe:
    def __init__(self, receta):
        self.recipe = receta
        self.id = self.get_recipe_id(self.recipe)
        self.information = self.get_recipe_information()
        self.ingredients = self.get_ingredients()
        self.most_popular_ingredient = self.popular_ingredient()


    def get_recipe_information(self):
        url = f"https://api.spoonacular.com/recipes/{id}/information?apiKey={api_key}&includeNutrition=false"
        info = requests.get(url).json()
        return info


    def get_ingredients(self):
        ingredients = self.information["extendedIngredients"]
        return ingredients

    def get_recipe_id(self, recipe):
        url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&query={recipe}"
        res = requests.get(url).json()
        results = res["results"][0]
        id = results["id"]
        return id   

    def popular_ingredient(self):
        ingredients = self.ingredients
        ingredients.sort(key=lambda x: x["amount"], reverse=True)
        return ingredients[0]


    def five_recepies(self, recipe):
        pass


recipe = Recipe("pasta")
# print(recipe.id)
# print(recipe.information)
print(recipe.ingredients)
# print(recipe.most_popular_ingredient)