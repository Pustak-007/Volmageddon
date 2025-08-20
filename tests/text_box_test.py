import matplotlib.pyplot as plt
x = list(x for x in range(3,30,3))
y = list (x**2 for x in x)
print(x)
print(y)
plt.plot(x,y)
plt.text(10,400,'lado kha mug',bbox = dict(boxstyle = 'round, pad = 0.5', facecolor = 'pink', alpha = 0.4), alpha = 0.9)
plt.show()