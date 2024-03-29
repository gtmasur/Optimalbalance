import matplotlib.pyplot as plt
import numpy as np

def update_hov(sim):

    sim.fig.suptitle(smart_time(sim.time))
    if sim.Nx > 1:
        sim.hov_h[:,:,sim.hov_count] = sim.soln.h[:,0,:-1]
        x = sim.x/1e3
    else:
        sim.hov_h[:,:,sim.hov_count] = sim.soln.h[0,:,:-1] 
        x = sim.y/1e3
    sim.hov_count += 1

