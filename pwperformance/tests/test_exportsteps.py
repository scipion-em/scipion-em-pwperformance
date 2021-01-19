import unittest

import pyworkflow
from pyworkflow.project import Manager, Project
# Get the manager
from pwperformance.main import Benchmark, codespeed


class TestExportSteps(unittest.TestCase):

    def testExportSteps(self):

        manager = Manager()
        stepsStats = dict()

        for project in manager.listProjects():
            projectFolder = manager.getProjectPath(project.projName)

            project = Project(pyworkflow.Config.getDomain(), projectFolder)
            project.load()


            for prot in project.getRuns():
                protName = prot.getClassName()
                for step in prot.loadSteps():
                    stepName= "-".join([prot.getClassPackageName(), protName, step.funcName.get()])
                    stepSeconds = step.getElapsedTime().total_seconds()
                    if stepName not in stepsStats:
                        stepsStats[stepName] = []

                    stepsStats[stepName].append(stepSeconds)

        # average steps
        for name in stepsStats:
            plugin, protClass, step = name.split("-")
            stepStats = stepsStats[name]
            mean = sum(stepStats) / len(stepStats)
            # DO not send mean values if higher than a threshold to keep chart in a decent visualization range
            # We are loosing long duration steps, probably due to large
            if mean < 30:
                bm = Benchmark(time=mean,
                           name= "-".join([protClass, step]))
                codespeed.sendData(bm)


