# 08-batch.py
# Deck 02: Programming with LLMs (Parallel and batch calls)
# Goal: run the structured recipe extraction across many PDFs in parallel.
# Save the JSON output so we can reuse it in later exercises.

# %% Import packages and load environment variable for API access
import chatlas
import dotenv

dotenv.load_dotenv()

# %% Read in all the recipes
from pyhere import here

recipe_files = list(here("data/recipes/text").glob("*"))
recipes = [f.read_text(encoding="utf-8") for f in recipe_files]

# %% Let's use the same Pydantic model from the last exercise
from typing import List, Optional

from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    name: str = Field(..., description="Name of the ingredient")
    quantity: str | None = Field(default=None, description="Quantity as provided")
    unit: Optional[str] = Field(
        None,
        description="Unit of measure, if applicable",
    )
    notes: Optional[str] = Field(
        None,
        description="Additional notes or preparation details",
    )


class Recipe(BaseModel):
    title: str
    description: str
    image_url: Optional[str] = Field(None, description="URL of an image of the dish")
    ingredients: List[Ingredient]
    instructions: List[str] = Field(..., description="Step-by-step instructions")

# %% Use a simple loop to process each recipe one at a time (can be slow and expensive!)
from tqdm import tqdm

def extract_recipe(recipe_text: str) -> Recipe:
    chat = chatlas.ChatAnthropic(model="claude-haiku-4-5")
    return chat.chat_structured(recipe_text, data_model=Recipe)

recipes_data: List[Recipe] = []
for recipe in tqdm(recipes):
    recipes_data.append(extract_recipe(recipe))

# %% What did we get?
[r.title for r in recipes_data]

# %% Can that be a polars DataFrame?
import polars as pl

recipes_df = pl.DataFrame([r.model_dump() for r in recipes_data], strict=False)
recipes_df

# %% We can save money by using the Batch API
#
# With the Batch API, results are processed asynchronously and are completed at
# some point, usually within a few minutes but at most within the next 24 hours.
# Because batching lets providers schedule requests more efficiently, it also
# costs less per token than the standard API.

# from chatlas import batch_chat_structured
# 
# chat = chatlas.ChatAnthropic(model="claude-haiku-4-5")
# res = batch_chat_structured(
#     chat=chat,
#     prompts=recipes,
#     data_model=Recipe,
#     path=here("data/recipes/batch_results_py_claude.json"),
# )

# %% Now, save the results to a JSON file in `data/recipes/recipes.json`
import json

recipes_structured = [r.model_dump() for r in recipes_data]
json.dump(recipes_structured, open(here("data/recipes/recipes.json"), "w"), indent=2)

# Once you've done that, you can open up `08-batch-app.py` and run the app to see
# your new recipe collection!