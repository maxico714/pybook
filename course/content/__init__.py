"""Curriculum modules, one file per module.

Each file exposes ``MODULE``.  ``curriculum.py`` imports all twelve explicitly,
so a missing module is an ImportError at build time rather than a silently
shorter course.
"""
