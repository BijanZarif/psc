import matplotlib
matplotlib.use('agg')
matplotlib.interactive(False)

import os
import pdb
import sys
import time
import argparse

from pylab import *

import histstack

from tunnel import *

parser = argparse.ArgumentParser()
parser.add_argument('nStart', type=int)
parser.add_argument('nEnd', type=int)
args = parser.parse_args()

assert args.nStart > args.nEnd
for iplot in range(args.nStart, args.nEnd - 1, -1):
    assert os.path.exists('w{0:06d}.npy'.format(iplot))

if os.path.exists('a{0:06d}.npy'.format(iplot)):
    a = grid.load('a{0:06d}.npy'.format(iplot))
else:
    a = grid.zeros([4])

figure(figsize=(28,10))

for iplot in range(args.nStart, args.nEnd, -1):
    nPrintsPerPlot = 500
    nStepPerPrint = 20
    history = histstack.HistoryStack(nPrintsPerPlot * nStepPerPrint, step)
    history.populate(grid.load('w{0:06d}.npy'.format(iplot - 1)))

    for i in range(nPrintsPerPlot * nStepPerPrint):
        a[1] += 0.1 * c0 * obstacle
        w = history.pop()
        a = step.adjoint(a, w)
    a.save('a{0:06d}.npy'.format(iplot - 1))
    clf()
    subplot(2,1,1); contourf(x._data.T, y._data.T, a[1]._data.T, 200);
    axis('scaled'); colorbar()
    subplot(2,1,2); contourf(x._data.T, y._data.T, a[2]._data.T, 200);
    axis('scaled'); colorbar()
    savefig('adj{0:06d}.png'.format(iplot - 1))

