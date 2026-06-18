# 10-plot-noise.py
# Deck 03: Prompt engineering and RAG (Prompt engineering and hallucinations)
# Goal: replace the mpg vs weight plot with random noise. Send the same prompt
# and see what the model says. Then work with a partner to coax the model into
# giving a "decent" interpretation of pure noise.

# %% Import packages and generate data
import chatlas
import dotenv
import numpy as np
from matplotlib import pyplot as plt
from math import floor, sqrt
from plotnine import aes, geom_point, ggplot, labs, theme_bw

dotenv.load_dotenv()

m = 32
g = floor(sqrt(m))
u = (np.arange(1, g + 1) - 0.5) / g
xx, yy = np.meshgrid(u, u)
grid = np.column_stack([xx.ravel(), yy.ravel()])

# small jitter to avoid perfect lattice, scaled to cell size
eps = 1.0 / (2.0 * sqrt(m))
jitter = np.random.uniform(-eps, eps, size=grid.shape)
grid_jitter = np.clip(grid + jitter, 0.0, 1.0)

x = grid_jitter[:, 0]
y = grid_jitter[:, 1]

# %% Make a plot
p = (
    ggplot(aes(x=x, y=y))
    + geom_point(color="steelblue", size=2)
    + labs(title="MPG vs Weight", x="Weight (1000 lb)", y="Miles per Gallon (mpg)")
    + theme_bw()
)
p.show()

# Register the plot with matplotlib's current figure
plt.figure(p.draw())

# %% Send the plot to the model and ask for an interpretation
chat = chatlas.ChatAnthropic()
chat.chat("Interpret this plot of mtcars. This may be faulty data that I was given.", chatlas.content_image_plot(),)