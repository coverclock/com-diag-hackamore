"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import time
import os

import Logger
import Configure
import ModelStandard
import ViewPrint
import ViewCurses
import Controller
import Manifold
import Multiplex

def body(manifold, inputs, outputs, logger = None):
    logger = Logger.logger() if logger == None else logger
    multiplex = Multiplex.Multiplex()
    controller = Controller.Controller(multiplex, manifold)
    logger.info("Main.body: STARTING.")
    while inputs:
        controller.loop(inputs, outputs)
        time.sleep(2.0)
        logger.info("Main.body: RESTARTING.")
    logger.info("Main.body: STOPPING.")

def main():
    logger = Logger.logger()
    sources = Configure.servers(logger)
    model = ModelStandard.ModelStandard()
    view = ViewCurses.ViewCurses(model) if "TERM" in os.environ else ViewPrint.ViewPrint(model)
    manifold = Manifold.Manifold(model, view)
    body(manifold, sources, sources)

if __name__ == "__main__":
    main()
