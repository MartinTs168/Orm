from typing import List

from sqlalchemy.orm import sessionmaker

from helpers import session_decorator
from models import engine, Employee, Recipe, Chef
from seed import recipes

Session = sessionmaker(bind=engine)

session = Session()


@session_decorator(session)
def create_recipe(name, ingredients, instructions):
    new_recipe = Recipe(
        name=name,
        ingredients=ingredients,
        instructions=instructions
    )
    session.add(new_recipe)
    #  no need for commit since it's in decorator


# for name, ingredients, instructions in recipes:
#     create_recipe(name, ingredients, instructions)
#
#
# recipes = session.query(Recipe).all()
#
# # Loop through each recipe and print its details
# for recipe in recipes:
#     print(f"Recipe name: {recipe.name}")

@session_decorator(session)
def update_recipe_by_name(name: str, new_name: str, new_ingredients: str, new_instructions: str):
    # recipe = session.query(Recipe).filter_by(name=name).first()
    #
    # recipe.name = new_name
    # recipe.ingredients = new_ingredients
    # recipe.instructions = new_instructions

    record_changed: int = (  # like bulk_update
        session.query(Recipe)
        .filter_by(name=name)
        .update({
            Recipe.name: new_name,
            Recipe.ingredients: new_ingredients,
            Recipe.instructions: new_instructions
        })
    )

    return record_changed


# Update a recipe by name
# update_recipe_by_name(
#     name="Spaghetti Carbonara",
#     new_name="Carbonara Pasta",
#     new_ingredients="Pasta, Eggs, Guanciale, Cheese",
#     new_instructions="Cook the pasta, mix with eggs, guanciale, and cheese"
# )
#
# # Query the updated recipe
# updated_recipe = session.query(Recipe).filter_by(name="Carbonara Pasta").first()
#
# # Print the updated recipe details
# print("Updated Recipe Details:")
# print(f"Name: {updated_recipe.name}")
# print(f"Ingredients: {updated_recipe.ingredients}")
# print(f"Instructions: {updated_recipe.instructions}")

@session_decorator(session)
def delete_recipe_by_name(name: str):
    records_changed = (
        session.query(Recipe)
        .filter_by(name=name)
        .delete()
    )

    return records_changed


@session_decorator(session, False)
def get_recipes_by_ingredient(ingredient_name: str) -> List:
    recipes = (
        session.query(Recipe)
        .where(Recipe.ingredients.ilike(f"%{ingredient_name}%"))
        .all()
    )

    return recipes


@session_decorator(session)
def swap_recipe_ingredients_by_name(first_recipe_name: str, second_recipe_name: str) -> None:
    first_recipe = (
        session.query(Recipe)
        .filter_by(name=first_recipe_name)
        .with_for_update()  # locks the object from being tampered with outside this session until it is closed
        .one()  # raises an exception if no record is found or more than one record is found
    )

    second_recipe = (
        session.query(Recipe)
        .filter_by(name=second_recipe_name)
        .with_for_update()
        .one()
    )

    first_recipe.ingredients, second_recipe.ingredients = second_recipe.ingredients, first_recipe.ingredients


@session_decorator(session)
def relate_recipe_with_chef_by_name(recipe_name: str, chef_name: str) -> str:
    recipe = (
        session.query(Recipe)
        .filter_by(name=recipe_name)
        .first()
    )

    if recipe and recipe.chef:
        raise Exception(f"Recipe: {recipe_name} already has a related chef")

    chef = (
        session.query(Chef)
        .filter_by(name=chef_name)
        .first()
    )
    recipe.chef = chef
    return f"Related recipe {recipe_name} with chef {chef_name}"


@session_decorator(session)
def get_recipes_with_chef() -> str:
    recipes = (
        session.query(Recipe.name, Chef.name)
        .join(Chef)
        .all()
    )

    result = []
    for recipe_name, chef_name in recipes:
        result.append(f"Recipe: {recipe_name} made by chef: {chef_name}")

    return "\n".join(result)


print(get_recipes_with_chef())
