import matplotlib
from matplotlib import pyplot as plt
import bornagain as ba
from bornagain import deg


class DrawObserver(ba.IFitObserver):
    """
    Draws fit progress every nth iteration.
    This class has to be attached to ba.FitSuite via attachObserver method.
    ba.FitSuite kernel will call DrawObserver's update() method every n'th iteration.
    It is up to the user what to do here.
    """

    def __init__(self, draw_every_nth=10):
        ba.IFitObserver.__init__(self, draw_every_nth)
        self.fig = plt.figure(figsize=(10.25, 7.69))
        self.fig.canvas.draw()
        plt.ion()

    def plot(self, data, title, nplot, min=1, max=1e6):
        plt.subplot(2, 2, nplot)
        plt.subplots_adjust(wspace=0.2, hspace=0.2)
        im = plt.imshow(
            data.getArray(),
            norm=matplotlib.colors.LogNorm(min, max),
            extent=[data.getXmin()/deg, data.getXmax()/deg,
                    data.getYmin()/deg, data.getYmax()/deg])
        plt.colorbar(im)
        plt.title(title)

    def update(self, fit_suite):
        self.fig.clf()
        real_data = fit_suite.getRealData()
        self.plot(real_data, "\"Experimental\" data",
                  nplot=1, min=1.0, max=real_data.getMaximum())
        self.plot(fit_suite.getSimulationData(), "Simulated data",
                  nplot=2, min=1.0, max=real_data.getMaximum())
        self.plot(fit_suite.getChiSquaredMap(), "Chi2 map",
                  nplot=3, min=0.001, max=10.0)

        plt.subplot(2, 2, 4)
        plt.title('Parameters')
        plt.axis('off')
        plt.text(0.01, 0.85, "Iterations  " + '{:d}     {:s}'.
                 format(fit_suite.numberOfIterations(),
                        fit_suite.minimizer().minimizerName()))
        plt.text(0.01, 0.75, "Chi2       " + '{:8.4f}'.format(fit_suite.getChi2()))
        for index, fitPar in enumerate(fit_suite.fitParameters()):
            plt.text(0.01, 0.55 - index*0.1,
                     '{:30.30s}: {:6.3f}'.format(fitPar.name(), fitPar.value()))
        plt.draw()
        plt.pause(0.01)

        if fit_suite.isLastIteration():
            plt.ioff()

