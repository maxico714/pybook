"""Assemble every module into one Course object.

Import order matters: modules are listed explicitly and the builder refuses to
run if one is missing, so a module can never be silently dropped.
"""
from __future__ import annotations

from .content import m01, m02, m03, m04, m05, m06, m07, m08, m09, m10, m11, m12
from .schema import Course, L

MODULE_SOURCES = [m01, m02, m03, m04, m05, m06, m07, m08, m09, m10, m11, m12]

COURSE = Course(
    id="pybook",
    title=L(
        "PyBook — Python, From Zero to Confident",
        "PyBook — पायथन, शून्य से आत्मविश्वास तक",
        "PyBook — Python, Zero se Confident tak",
    ),
    subtitle=L(
        "A notebook course: every core keyword and concept, each lesson with an "
        "introduction, a real-life example, runnable code and a quiz gate.",
        "एक नोटबुक कोर्स: हर मुख्य कीवर्ड और कॉन्सेप्ट, हर लेसन में परिचय, "
        "रोज़मर्रा का उदाहरण, चलने वाला कोड और क्विज़ गेट।",
        "Ek notebook course: har core keyword aur concept, har lesson me intro, "
        "real-life example, chalne wala code aur quiz gate.",
    ),
    modules=[source.MODULE for source in MODULE_SOURCES],
)


def curriculum_dict() -> dict:
    return COURSE.to_dict()
