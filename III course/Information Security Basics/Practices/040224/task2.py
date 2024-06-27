import numpy as np
import plotly.graph_objects as go

np.random.seed(1)
fig = go.Figure()
y0 = np.random.randn(50)
y1 = np.random.randn(50)
y2 = np.random.randn(50)
y3 = np.random.randn(50)

fig.add_trace(go.Box(y=y0))
fig.add_trace(go.Box(y=y1))

fig.add_trace(go.Box(x=y2))
fig.add_trace(go.Box(y=y3))


fig.show()
