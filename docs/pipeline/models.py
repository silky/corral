#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created at 2015-12-09T16:33:40.827063 by corral 0.0.1


# =============================================================================
# DOCS
# =============================================================================

"""pipeline database models

"""

# =============================================================================
# IMPORTS
# =============================================================================

from corral import db


# =============================================================================
# MODELS (Put your models below)
# =============================================================================

class Example(db.Model):

    __tablename__ = 'Example'

    id = db.Column(db.Integer, primary_key=True)
