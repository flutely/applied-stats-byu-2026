# 07-structured-output.py
# Deck 02: Programming with LLMs (Structured output)
# Goal: extract structured fields (ingredients, steps, yield, prep time) from a
# recipe using a Pydantic model with chatlas.

# %% Import packages and load environment variable for API access
import chatlas
import dotenv
from pyhere import here

dotenv.load_dotenv()

# %% Read in a recipe markdown example
recipe_txt = here("data/recipes/text/")
txt_cheesecake = recipe_txt / "PhillyCheesesteak.md"
print(txt_cheesecake)

# %% Markdown for example output
# Here's an example of the structured output we want to achieve for a single
# recipe:
#
# ```json
# {
#   "title": "Spicy Mango Salsa Chicken",
#   "description": "A flavorful and vibrant chicken dish...",
#   "ingredients": [
#     {
#       "name": "Chicken Breast",
#       "quantity": "4",
#       "unit": "medium",
#       "notes": "Boneless, skinless"
#     },
#     {
#       "name": "Lime Juice",
#       "quantity": "2",
#       "unit": "tablespoons",
#       "notes": "Fresh"
#     }
#   ],
#   "instructions": [
#     "Preheat grill to medium-high heat.",
#     "In a bowl, combine ...",
#     "Season chicken breasts with salt and pepper.",
#     "Grill chicken breasts for 6-8 minutes per side, or until cooked through.",
#     "Serve chicken topped with the spicy mango salsa."
#   ]
# }
# ```

# %% Make a Pydantic model to represent the structured output we want from the recipe
from typing import List, Optional
from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    name: str = Field(..., description="Name of the ingredient in shakespeare speak")
    quantity: str = Field(
        ...,
        description="Quantity as provided (kept as string to allow ranges or fractions) but with shakespearean measures",
    )
    unit: Optional[str] = Field(
        None,
        description="Unit of measure, if applicable in shakespeare speak (e.g., 'cup' might be 'grog mug')",
    )
    notes: Optional[str] = Field(
        None,
        description="Additional notes or preparation details in shakespeare speak",
    )


class Recipe(BaseModel):
    title: str
    description: str
    ingredients: List[Ingredient]
    instructions: List[str] = Field(..., description="Step-by-step instructions")

# %% Pass the recipe text and the Pydantic model to get structured output
chat = chatlas.ChatAnthropic()
recipe = chat.chat_structured(txt_cheesecake.read_text(encoding="utf-8"), data_model=Recipe)

# %% We get an instance of the Pydantic model, so you can access fields directly
recipe.title

# %% Or you can convert it to JSON
print(recipe.model_dump_json(indent=2))
