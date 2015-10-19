#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# IMPORT
# =============================================================================

import collections


# =============================================================================
# FUNCTIONS
# =============================================================================

def to_namedtuple(name, **d):
    keys = list(d.keys())
    namedtuple = collections.namedtuple(name, d)
    return namedtuple(**d)
