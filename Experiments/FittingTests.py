from lmfit.models import GaussianModel
import HelperFunctions
import matplotlib.pyplot as plt

energy, sint, phase = HelperFunctions.get_data()

mod = GaussianModel()
prams = mod.make_params(center=dict(value=1.8),
                               sigma=dict(value=3, min=0),
                               amplitude=dict(value=0.2e-7, min=0))

out = mod.fit(sint,prams, x = energy)

plt.plot(energy, sint)
plt.plot(energy, out.best_fit -1e-10)
plt.show()