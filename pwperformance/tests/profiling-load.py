import os
import sys
import tempfile
from pwperformance.main import Timer, Benchmark, codespeed
import pyworkflow
from pyworkflowtests.protocols import ProtOutputTest
from pyworkflow.project import Manager, Project


#
# numProts = 300
# # Create a new project
# manager = Manager()
#
# if len(sys.argv)>1:
#     projectFolder= sys.argv[1]
#     benchmarkName = "%s load." % projectFolder
#     print("Profiling %s" % projectFolder)
#
# elif len(sys.argv) == 1:
#     projectFolder = tempfile.mkdtemp()
#     benchmarkName = "Project %s prots load" % numProts
#     print("Project folder at: %s" % projectFolder)
#     ct = Timer()
#     ct.tic()
#     project = manager.createProject(os.path.basename(projectFolder), location=os.path.dirname(projectFolder))
#
#     previousProt = None
#     currentProt = None
#     # Add protocols
#     for count in range(numProts):
#         args = dict()
#
#         newProt = project.newProtocol(ProtOutputTest, iBoxSize=10)
#
#         if currentProt is not None:
#             previousProt = currentProt
#
#         currentProt = newProt
#
#         currentProt._store()
#     ct.toc()
#
#     bm = Benchmark(time=ct.getElapsedTime().total_seconds(),
#                    name="Project creation %s prots" % numProts)
#     codespeed.sendData(bm)
#
# t = Timer()
# t.tic()
# project = Project(pyworkflow.Config.getDomain(), projectFolder)
# project.load()
# project.getRuns()
#
# bm = Benchmark(time=t.getElapsedTime().total_seconds(),
#                name=benchmarkName)
# codespeed.sendData(bm)
#
#
#
