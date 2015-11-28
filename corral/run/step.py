#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
import inspect
import multiprocessing

from .. import conf, db, util, exceptions
from ..core import logger

from .base import Processor, Runner


# =============================================================================
# STEP CLASSES
# =============================================================================

class StepRunnerBase(Runner):

    def setup(self, step_cls):
        if not (inspect.isclass(step_cls) and issubclass(step_cls, Step)):
            msg = "step_cls '{}' must be subclass of 'corral.run.Step'"
            raise TypeError(msg.format(step_cls))
        self.step_cls = step_cls

    def run(self):
        step_cls = self.step_cls
        logger.info("Executing step '{}'".format(step_cls))
        with db.session_scope() as session, step_cls(session) as step:
            for obj in step.generate():
                step.validate(obj)
                generator = step.process(obj) or []
                if not hasattr(generator, "__iter__"):
                    generator = (generator,)
                for proc_obj in generator:
                    step.validate(proc_obj)
                    step.save(proc_obj)
                step.save(obj)
        logger.info("Done!")


class StepRunner(StepRunnerBase, multiprocessing.Process):
    pass


class Step(Processor):

    runner_class = StepRunnerBase

    model = None
    conditions = None

    ordering = None
    offset, limit = None, None

    def generate(self):
        if self.model is None or self.conditions is None:
            clsname = type(self).__name__
            raise NotImplementedError(
                "'{}' subclass with a default generate must redefine "
                "'model' and 'conditions' class-attributes".format(clsname))
        query = self.session.query(self.model).filter(*self.conditions)
        if self.ordering is not None:
            query = query.order_by(*self.ordering)
        if self.offset is not None:
            query = query.offset(self.offset)
        if self.limit is not None:
            query = query.limit(self.limit)
        return query

    @abc.abstractmethod
    def process(self, obj):
        raise NotImplementedError()  # pragma: no cover


# =============================================================================
# FUNCTIONS
# =============================================================================

def load_steps():
    steps = []
    logger.debug("Loading Steps Classes")
    for import_string in conf.settings.STEPS:
        cls = util.dimport(import_string)
        if not (inspect.isclass(cls) and issubclass(cls, Step)):
            msg = "STEP '{}' must be subclass of 'corral.run.Step'"
            raise exceptions.ImproperlyConfigured(msg.format(import_string))
        steps.append(cls)
    return tuple(steps)


def execute_step(step_cls, sync=False):
    if not (inspect.isclass(step_cls) and issubclass(step_cls, Step)):
        msg = "step_cls '{}' must be subclass of 'corral.run.Step'"
        raise TypeError(msg.format(step_cls))

    runner = step_cls.runner_class()
    runner.setup(step_cls)
    if sync:
        runner.run()
    else:
        runner.start()
    return runner
