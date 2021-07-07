# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright (c) Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# ----------------------------------------------------------------------------

"""pyls-spyder plugin tests."""

# PyLS imports
from pyls import uris
from pyls.workspace import Document

# pytest imports
import pytest
from unittest.mock import MagicMock

# Local imports
from pyls_spyder.plugin import pyls_document_symbols, pyls_folding_range


DOC_URI = uris.from_fs_path(__file__)
DOC = """
# %%
# ---- Imports
import os
import sys

# <codecell> Other cell
# ----
def a():
    #### Block comment on a
    # %%% Cell inside a
    for i in range(0, 10):
        # %%%% Cell
        pass

# %%%
def b():
    #---- Pass inside b
    pass

# In[25]
####

#%% Invalid comments
#----
# ---------- This should not work
###### This either
#%% Empty cell
"""


@pytest.fixture
def workspace():
    return MagicMock()


@pytest.fixture
def config():
    return MagicMock()


def test_cell_block_symbols(config, workspace):
    document = Document(DOC_URI, workspace, DOC)
    symbols = pyls_document_symbols(config, workspace, document)
    expected = [
        ('Unnamed cell 1', 1, 22, 225),
        ('Imports', 2, 2, 224),
        ('Other cell', 6, 6, 225),
        ('Unnamed comment 1', 7, 7, 224),
        ('Block comment on a', 9, 9, 224),
        ('Cell inside a', 10, 14, 225),
        ('Cell', 12, 14, 225),
        ('Unnamed cell 2', 15, 22, 225),
        ('Pass inside b', 17, 17, 224),
        ('25', 20, 20, 225),
        ('Unnamed comment 2', 21, 21, 224),
        ('Invalid comments', 23, 26, 225),
        ('Unnamed comment 3', 24, 24, 224),
        ('Empty cell', 27, 27, 225)
    ]
    test_results = []
    for symbol in symbols:
        name = symbol['name']
        location = symbol['location']
        sym_range = location['range']
        start = sym_range['start']['line']
        end = sym_range['end']['line']
        kind = symbol['kind']
        test_results.append((name, start, end, kind))
    assert expected == test_results


def test_ungroup_cell_symbols(config, workspace):
    document = Document(DOC_URI, workspace, DOC)
    config.plugin_settings = lambda _: {'group_cells': False}
    symbols = pyls_document_symbols(config, workspace, document)
    expected = [
        ('Unnamed cell 1', 1, 1, 225),
        ('Imports', 2, 2, 224),
        ('Other cell', 6, 6, 225),
        ('Unnamed comment 1', 7, 7, 224),
        ('Block comment on a', 9, 9, 224),
        ('Cell inside a', 10, 10, 225),
        ('Cell', 12, 12, 225),
        ('Unnamed cell 2', 15, 15, 225),
        ('Pass inside b', 17, 17, 224),
        ('25', 20, 20, 225),
        ('Unnamed comment 2', 21, 21, 224),
        ('Invalid comments', 23, 23, 225),
        ('Unnamed comment 3', 24, 24, 224),
        ('Empty cell', 27, 27, 225)
    ]
    test_results = []
    for symbol in symbols:
        name = symbol['name']
        location = symbol['location']
        sym_range = location['range']
        start = sym_range['start']['line']
        end = sym_range['end']['line']
        kind = symbol['kind']
        test_results.append((name, start, end, kind))
    assert expected == test_results


def test_disable_block_comments(config, workspace):
    document = Document(DOC_URI, workspace, DOC)
    config.plugin_settings = lambda _: {'enable_block_comments': False}
    symbols = pyls_document_symbols(config, workspace, document)
    expected = [
        ('Unnamed cell 1', 1, 22, 225),
        ('Other cell', 6, 6, 225),
        ('Cell inside a', 10, 14, 225),
        ('Cell', 12, 14, 225),
        ('Unnamed cell 2', 15, 22, 225),
        ('25', 20, 20, 225),
        ('Invalid comments', 23, 26, 225),
        ('Empty cell', 27, 27, 225)
    ]
    test_results = []
    for symbol in symbols:
        name = symbol['name']
        location = symbol['location']
        sym_range = location['range']
        start = sym_range['start']['line']
        end = sym_range['end']['line']
        kind = symbol['kind']
        test_results.append((name, start, end, kind))
    assert expected == test_results


def test_cell_folding_regions(config, workspace):
    document = Document(DOC_URI, workspace, DOC)
    regions = pyls_folding_range(config, workspace, document)
    expected = [
        (1, 22),
        (6, 9),
        (10, 14),
        (12, 14),
        (15, 22),
        (20, 22),
        (23, 26),
        (27, 27)
    ]
    test_results = []
    for region in regions:
        start = region['startLine']
        end = region['endLine']
        test_results.append((start, end))
    assert expected == test_results
