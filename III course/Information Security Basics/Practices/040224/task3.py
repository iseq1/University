import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

x = [-5,-5,-3,-1,-1,None ,1,3,1,1,3,1,1,3, None, 5,5,7,7]
y = [1,5,3,5,1,None ,1,1,1,3,3,3,5,5, None, 1,5,5,1]

plt.plot(x,y)
plt.xlabel('x - axes')
plt.ylabel('y - axes')
plt.title('My first graph!')
plt.show()
