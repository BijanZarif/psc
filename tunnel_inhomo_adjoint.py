import matplotlib
matplotlib.use('agg')
matplotlib.interactive(False)

import os
import pdb
import sys
import time
import argparse

from pylab import *

sys.path.append('..')
import psarray
import histstack

from tunnel import *

def orthogonalize_wrt(a, a_homo):
    # nondimensionalize
    w0 = np.array([np.sqrt(rho0), np.sqrt(rho0) * u0, np.sqrt(rho0) * u0, p0])
    a = a * w0
    a_homo = a_homo * w0

    # orthogonalize
    b = grid.sum(a[np.newaxis,:] * a_homo).sum(1) \
      / grid.sum(a_homo * a_homo).sum(1)
    Linv = np.linalg.inv(L) 
    a = (a[np.newaxis,:,:] * Linv[:,:,np.newaxis]).sum(1)

    return a_homo / w0, b  # re-dimensionalize

parser = argparse.ArgumentParser()
parser.add_argument('nStart', type=int)
parser.add_argument('nEnd', type=int)
parser.add_argument('mAdj', type=int)
args = parser.parse_args()

assert args.nStart > args.nEnd
assert args.mAdj > 1

for iplot in range(args.nStart, args.nEnd - 1, -1):
    assert os.path.exists('w{0:06d}.npy'.format(iplot))

if os.path.exists('a{0:06d}-{1:03d}.npy'.format(iplot, args.mAdj)):
    a = grid.load('a{0:06d}-{1:03d}.npy'.format(iplot, args.mAdj))
else:
    a = grid.random([args.mAdj, 4])

figure(figsize=(28,10))

for iplot in range(args.nStart, args.nEnd, -1):
    nPrintsPerPlot = 500
    nStepPerPrint = 20
    history = histstack.HistoryStack(nPrintsPerPlot * nStepPerPrint, step)
    history.populate(grid.load('w{0:06d}.npy'.format(iplot - 1)))

    for i in range(nPrintsPerPlot * nStepPerPrint):
        w = history.pop()
        for iAdj in range(args.mAdj):
            a[iAdj] = step.adjoint(a[iAdj], w)

    a, L = orthogonalize(a)

    a.save('a{0:06d}-{1:03d}.npy'.format(iplot - 1, args.mAdj))
    np.save('L{0:06d}-{1:03d}.npy'.format(iplot - 1, args.mAdj), L)

    for iAdj in range(args.mAdj):
        clf()
        subplot(2,1,1); contourf(x._data.T, y._data.T, a[iAdj,1]._data.T, 200);
        axis('scaled'); colorbar()
        subplot(2,1,2); contourf(x._data.T, y._data.T, a[iAdj,2]._data.T, 200);
        axis('scaled'); colorbar()
        savefig('adj{0:06d}-{1:03d}-{2:03d}.png'.format(iplot - 1, 
                        args.mAdj, iAdj))

