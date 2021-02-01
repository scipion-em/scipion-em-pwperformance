import os
import tkinter as tk
import unittest

import pyworkflow.gui as pwgui
import pyworkflow as pw
import pyworkflow.project as pwobj
from pwperformance.main import Timer, Benchmark, codespeed


class TestProfilingLoadGUI(unittest.TestCase):
    root = tk.Tk()
    def createCanvas(self):

        canvas = pwgui.Canvas(self.root, width=800, height=800,
                              tooltipDelay=1000,
                              name="runs_canvas",
                              takefocus=True,
                              highlightthickness=0)

        canvas.frame.grid(row=0, column=0, sticky='nsew')
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        return canvas

    def getRunsGraph(self, project):
        settingsPath = os.path.join(project.path, project.settingsPath)
        if os.path.exists(settingsPath):
            settings = project.getSettings()

        project.getRuns()
        runsGraph = project.getRunsGraph(refresh=True, checkPids=True)

        # Create empty nodeInfo for new runs
        self.numberofprotocols = 0
        for node in runsGraph.getNodes():
            self.numberofprotocols += 1
            nodeId = node.run.getObjId() if node.run else 0
            nodeInfo = settings.getNodeById(nodeId)
            if nodeInfo is None:
                settings.addNode(nodeId, x=0, y=0, expanded=True)
        return runsGraph

    def findProjects(self):
        self.projectsPath = os.environ.get("PROFILING_PROJECTS_PATH", "/home/yunior/profilingProjects/")

        if self.projectsPath is not None:
            for base, dirs, files in os.walk(self.projectsPath):
                return dirs

    def testLoadProjectGUI(self):
        t = Timer()
        localProjects = self.findProjects()
        t.tic()
        for projectFolder in localProjects:
            print("Profiling %s" % projectFolder)
            project = pwobj.Project(pw.Config.getDomain(),
                                    os.path.join(self.projectsPath,
                                                 projectFolder))
            try:
                project.load()
                canvas = self.createCanvas()
                runsGraph = self.getRunsGraph(project)
                layout = pwgui.LevelTreeLayout()
                canvas.drawGraph(runsGraph, layout, drawNode=None)
                loadProjectTime = t.getElapsedTime()
                bm = Benchmark(time=loadProjectTime.total_seconds(),
                               name="Load project %s with GUI with %s protocols" % (
                               projectFolder, self.numberofprotocols))
                codespeed.sendData(bm)
            except Exception as e:
                print("Error loading the project %s" % projectFolder)



