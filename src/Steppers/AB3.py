import numpy as np
from .Euler import Euler
from .AB2 import AB2

def AB3_real(sim): 
        
    if sim.nfluxes < 2:
        sim.nfluxes = 2
        
    if len(sim.fluxes.u) == 0:

        Euler(sim)

    elif len(sim.fluxes.u) == 1:

        AB2(sim)

    elif len(sim.fluxes.u) == 2:

        # Compute the fluxes
        sim.flux()

        if sim.adaptive:
            # Compute the weights for the adaptive delta(t)
            # Adams-Bashforth 3 scheme
            tp = sim.time + sim.dt
            tn = sim.time

            gam1 = 3*tn**2 + 3*tn*sim.dt + sim.dt**2 # (tp**3 - tn**3)/dt
            gam2 = 2*sim.time + sim.dt # (tp**2 - tn**2)/dt
            gam3 = 1.   # (tp - tn)/dt

            a  = sim.time - sim.dts[0]
            b  = sim.time - sim.dts[0] - sim.dts[1]

            w0 = sim.dt*((1./3)*gam1 - 0.5*gam2*(a+b) + a*b*gam3) / (sim.dts[0]*(sim.dts[0]+sim.dts[1]))

            a  = sim.time
            b  = sim.time - sim.dts[0] - sim.dts[1]

            w1 = sim.dt*((1./3)*gam1 - 0.5*gam2*(a+b) + a*b*gam3) / (-sim.dts[0]*sim.dts[1])

            a  = sim.time
            b  = sim.time - sim.dts[0]

            w2 = sim.dt*((1./3)*gam1 - 0.5*gam2*(a+b) + a*b*gam3) / ((sim.dts[0]+sim.dts[1])*sim.dts[1])
        else:
            # Compute the weights for the fixed delta(t)
            # Adams-Bashforth 3 scheme
            w0 =  23./12.*sim.dt
            w1 = -16./12.*sim.dt
            w2 =   5./12.*sim.dt

        # Evolve the system
        sim.soln.u += w0*sim.curr_flux.u + w1*sim.fluxes.u[0] + w2*sim.fluxes.u[1]
        sim.soln.v += w0*sim.curr_flux.v + w1*sim.fluxes.v[0] + w2*sim.fluxes.v[1]
        sim.soln.h += w0*sim.curr_flux.h + w1*sim.fluxes.h[0] + w2*sim.fluxes.h[1]
        
        # Store the appropriate histories.
        if sim.nfluxes == 2:
            sim.fluxes.u = [sim.curr_flux.u.copy(), sim.fluxes.u[0].copy()]
            sim.fluxes.v = [sim.curr_flux.v.copy(), sim.fluxes.v[0].copy()]
            sim.fluxes.h = [sim.curr_flux.h.copy(), sim.fluxes.h[0].copy()]
            sim.dts    = [sim.dt, sim.dts[0]]
        else:
            sim.fluxes.u = [sim.curr_flux.u.copy()] + sim.fluxes.u
            sim.fluxes.v = [sim.curr_flux.v.copy()] + sim.fluxes.v
            sim.fluxes.h = [sim.curr_flux.h.copy()] + sim.fluxes.h
            sim.dts = [sim.dt] + sim.dts
            
def AB3_ramp(sim): 
        
    if sim.ramp_nfluxes < 2:
        sim.ramp_nfluxes = 2
        
    if len(sim.ramp_fluxes.u) == 0:

        Euler(sim)

    elif len(sim.ramp_fluxes.u) == 1:

        AB2(sim)

    elif len(sim.ramp_fluxes.u) == 2:

        # Compute the fluxes
        sim.ramp_flux(sim)

        if sim.adaptive:
            # Compute the weights for the adaptive delta(t)
            # Adams-Bashforth 3 scheme
            tp = sim.ramp_time + sim.ramp_dt
            tn = sim.ramp_time

            gam1 = 3*tn**2 + 3*tn*sim.ramp_dt + sim.ramp_dt**2 # (tp**3 - tn**3)/dt
            gam2 = 2*sim.ramp_time + sim.ramp_dt # (tp**2 - tn**2)/dt
            gam3 = 1.   # (tp - tn)/dt

            a  = sim.ramp_time - sim.ramp_dts[0]
            b  = sim.ramp_time - sim.ramp_dts[0] - sim.ramp_dts[1]

            w0 = sim.ramp_dt*((1./3)*gam1 - 0.5*gam2*(a+b) + a*b*gam3) / (sim.ramp_dts[0]*(sim.ramp_dts[0]+sim.ramp_dts[1]))

            a  = sim.ramp_time
            b  = sim.ramp_time - sim.ramp_dts[0] - sim.ramp_dts[1]

            w1 = sim.ramp_dt*((1./3)*gam1 - 0.5*gam2*(a+b) + a*b*gam3) / (-sim.ramp_dts[0]*sim.ramp_dts[1])

            a  = sim.ramp_time
            b  = sim.ramp_time - sim.ramp_dts[0]

            w2 = sim.ramp_dt*((1./3)*gam1 - 0.5*gam2*(a+b) + a*b*gam3) / ((sim.ramp_dts[0]+sim.ramp_dts[1])*sim.ramp_dts[1])
        else:
            # Compute the weights for the fixed delta(t)
            # Adams-Bashforth 3 scheme
            w0 =  23./12.*sim.ramp_dt
            w1 = -16./12.*sim.ramp_dt
            w2 =   5./12.*sim.ramp_dt

        # Evolve the system
        sim.ramp_soln.u += w0*sim.ramp_curr_flux.u + w1*sim.ramp_fluxes.u[0] + w2*sim.ramp_fluxes.u[1]
        sim.ramp_soln.v += w0*sim.ramp_curr_flux.v + w1*sim.ramp_fluxes.v[0] + w2*sim.ramp_fluxes.v[1]
        sim.ramp_soln.h += w0*sim.ramp_curr_flux.h + w1*sim.ramp_fluxes.h[0] + w2*sim.ramp_fluxes.h[1]
        
        # Store the appropriate histories.
        if sim.ramp_nfluxes == 2:
            sim.ramp_fluxes.u = [sim.ramp_curr_flux.u.copy(), sim.ramp_fluxes.u[0].copy()]
            sim.ramp_fluxes.v = [sim.ramp_curr_flux.v.copy(), sim.ramp_fluxes.v[0].copy()]
            sim.ramp_fluxes.h = [sim.ramp_curr_flux.h.copy(), sim.ramp_fluxes.h[0].copy()]
            sim.ramp_dts    = [sim.ramp_dt, sim.ramp_dts[0]]
        else:
            sim.ramp_fluxes.u = [sim.ramp_curr_flux.u.copy()] + sim.ramp_fluxes.u
            sim.ramp_fluxes.v = [sim.ramp_curr_flux.v.copy()] + sim.ramp_fluxes.v
            sim.ramp_fluxes.h = [sim.ramp_curr_flux.h.copy()] + sim.ramp_fluxes.h
            sim.ramp_dts = [sim.ramp_dt] + sim.ramp_dts
            
def AB3(sim):

    if sim.system == 'Real':
        return AB3_real(sim)
    elif sim.system == 'Ramped':
        return AB3_ramp(sim)
            
