# 05-vision.py
# Deck 02: Programming with LLMs (Multi-modal input)
# Goal: pass an image of food and ask for recipe suggestions.

# %% Import packages and load environment variable for API access
import chatlas
import dotenv
from pyhere import here

dotenv.load_dotenv()

# %% Read in some recipe images
recipe_images = here("data/recipes/images/")
img_pancake = recipe_images / "VeryGrossPancakes.jpg"
img_mac_cheese = recipe_images / "CreamyCrockpotMacAndCheese.jpg"

# %% Pass the image to the chat and ask for a recipe title and description
chat = chatlas.ChatAnthropic()
chat.chat(
    "Give the food in this image a creative recipe title and description.",
    chatlas.content_image_file(img_pancake),
)

# # %% Pass a different image and ask for a recipe again
# chat = chatlas.ChatAnthropic()
# chat.chat(
#     "Write a recipe to make the food in this image.",
#     chatlas.content_image_file(img_mac_cheese),
# )