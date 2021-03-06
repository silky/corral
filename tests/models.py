#!/usr/bin/env python
# -*- coding: utf-8 -*-

from corral import db


# =============================================================================
# YOUR MODELS HERE
# =============================================================================

class SampleModel(db.Model):

    __tablename__ = 'SampleModel'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True, unique=True)

    def __eq__(self, obj):
        return (
            isinstance(obj, SampleModel) and
            obj.name == self.name and obj.id == self.id)
