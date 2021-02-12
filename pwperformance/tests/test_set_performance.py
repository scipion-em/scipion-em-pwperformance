import sys


# Initialize scipion environment
import tempfile
import unittest

from pwperformance.main import Timer, Benchmark, BENCHMARK, codespeed
from pwem.objects import SetOfCoordinates, Coordinate, SetOfParticles, Integer, Particle, Acquisition, Micrograph, Movie
import os
from  datetime import timedelta

from pyworkflow.tests import DataSet


class TestSetPerformanceSteps(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dataset = DataSet.getDataSet('xmipp_tutorial')
        cls.moviewset = DataSet.getDataSet('jmbFalconMovies')

        cls.mic1 = cls.dataset.getFile('mic1')
        cls.particlesStk = os.path.join(cls.dataset.getPath(), 'particles', 'BPV_1386.stk')
        cls.movieFn = cls.moviewset.getFile("movie1")

    def basiccoordsFactory(self, iteration):
        # newCoord =  Coordinate(x=i, y=i)
        # To avoid dict get
        newCoord = Coordinate()
        newCoord.setX(iteration)
        newCoord.setY(iteration)
        return newCoord

    def testBasicCoordinatesSet(self):

        measureSetPerformance(SetOfCoordinates, self.basiccoordsFactory, "basic-coords")

    def testExtendedCoordinatesSet(self):

        def coordsFactory(iteration):
            # newCoord =  Coordinate(x=i, y=i)
            # To avoid dict get
            newCoord = Coordinate()
            newCoord.setX(iteration)
            newCoord.setY(iteration)
            newCoord.extra1 = Integer(1)
            newCoord.extra2 = Integer(1)
            newCoord.extra3 = Integer(1)
            newCoord.extra4 = Integer(1)
            newCoord.extra5 = Integer(1)
            newCoord.extra6 = Integer(1)
            newCoord.extra7 = Integer(1)
            newCoord.extra8 = Integer(1)
            newCoord.extra9 = Integer(1)
            newCoord.extra10 = Integer(1)

            return newCoord

        measureSetPerformance(SetOfCoordinates, coordsFactory, "extended-10-coords")

    def testSuperExtendedCoordinatesSet(self):

        def coordsFactory(iteration):
            # newCoord =  Coordinate(x=i, y=i)
            # To avoid dict get
            newCoord = Coordinate()
            newCoord.setX(iteration)
            newCoord.setY(iteration)
            newCoord.extra1 = Integer(1)
            newCoord.extra2 = Integer(1)
            newCoord.extra3 = Integer(1)
            newCoord.extra4 = Integer(1)
            newCoord.extra5 = Integer(1)
            newCoord.extra6 = Integer(1)
            newCoord.extra7 = Integer(1)
            newCoord.extra8 = Integer(1)
            newCoord.extra9 = Integer(1)
            newCoord.extra10 = Integer(1)

            newCoord.extra11 = Integer(1)
            newCoord.extra12 = Integer(1)
            newCoord.extra13 = Integer(1)
            newCoord.extra14 = Integer(1)
            newCoord.extra15 = Integer(1)
            newCoord.extra16 = Integer(1)
            newCoord.extra17 = Integer(1)
            newCoord.extra18 = Integer(1)
            newCoord.extra19 = Integer(1)
            newCoord.extra20 = Integer(1)


            return newCoord

        measureSetPerformance(SetOfCoordinates, coordsFactory, "extended-20-coords", numberofitems=10**6)

    def testBasicMicsSetPerformance(self):

        def micsFactory(index):
            newMic = Micrograph(location=self.mic1)
            return newMic

        measureSetPerformance(SetOfParticles, micsFactory, "basic mics")


    def testBasicMoviesSetPerformance(self):

        def moviesFactory(index):
            newMovie = Movie(location=self.movieFn)
            return newMovie

        measureSetPerformance(SetOfParticles, moviesFactory, "basic movies")


    def testBasicParticlesSetPerformance(self):

        def particlesFactory(index):
            newParticle = Particle(location=(1,self.particlesStk))
            return newParticle

        measureSetPerformance(SetOfParticles, particlesFactory, "basic particles")


    def testComplexParticlesSetPerformance(self):

        def particlesFactory(index):
            newParticle = Particle(location=(1,self.particlesStk))
            newParticle.setCoordinate(Coordinate(x=1,y=2))
            newParticle.setAcquisition(Acquisition())
            return newParticle

        measureSetPerformance(SetOfParticles, particlesFactory, "complex particles")

    def testUsingGet(self):
        """ This benchmarks the time accessing an item as a dictionary, like set[id]."""
        items = 100
        soc = createSet(SetOfCoordinates)
        createItems(soc, self.basiccoordsFactory, numberofitems=items)
        t = Timer("A %s Set.__item__ calls" % items)
        t.tic()
        for id in range(1,items+1):
            soc[id]
        t.toc()
        bm = Benchmark(time=t.getElapsedTime().total_seconds(),
                       name="A %s Set.__item__ calls" % items)

        codespeed.sendData(bm)

def measureSetPerformance(setClass, itemFactory, performanceTag, numberofitems=100000):
    """ Measures instantiation, persistence and iteration of a set, sending data to a codespeed benchmark server"""

    newSet = createSet(setClass)

    createItems(newSet, itemFactory, numberofitems=numberofitems, performanceTag=performanceTag)

    measureSetIteration(newSet, performanceTag)


def createItems(set, itemfactory, numberofitems=100000, performanceTag=None):
    """ Create X items using numberofitems and the itemfactory method and reports its
    instantiation time and persistence time to the benchmark server
    :parameter set: Set instance to be used
    :parameter itemfactory: method to call to create a specific item. Receives the index of the iteration
    :parameter performanceTag: tag to use to create the benchmark name"""

    # To hold sum elapsed time
    creation = timedelta()
    append = timedelta()

    t = Timer()
    for i in range(numberofitems):
        t.tic()
        newItem = itemfactory(i)
        creation += t.getElapsedTime()
        t.tic()
        set.append(newItem)
        append += t.getElapsedTime()

    set.write()

    if performanceTag:

        bm = Benchmark(time=creation.total_seconds(),
                       name="Instantiation of %s %s" % (numberofitems, performanceTag))

        codespeed.sendData(bm)

        bm = Benchmark(time=append.total_seconds(),
                       name="Persistence of %s %s" % (numberofitems, performanceTag))

        codespeed.sendData(bm)

        measureSetIteration(set, performanceTag)

def createSet(setClass):
    """ Create a set based on the setClass in the system temporary folder"""

    tmpFolder = tempfile.gettempdir()
    setFile = str(setClass.__name__) +  "%s.sqlite"
    sqliteFile = os.path.join(tmpFolder, setFile % "")

    if os.path.exists(sqliteFile):
        os.remove(sqliteFile)

    return setClass.create(tmpFolder, template=setFile)


def measureSetIteration(set, performanceTag):
    """ Measures the time  taken to iterate over the set passed.
    :parameter set set to iterate on
    :parameter performanceTag: text to name the benchmark"""

    iterT = Timer()
    iterT.tic()
    for item in set.iterItems():
        pass
    iterT.toc()
    bm = Benchmark(time=iterT.getElapsedTime().total_seconds(),
                   name="Iteration-%s" % performanceTag)
    codespeed.sendData(bm)
