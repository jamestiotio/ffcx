"""
Compiler stage 1: Analysis
--------------------------

This module implements the analysis/preprocessing of variational
forms, including automatic selection of elements, degrees and
form representation type.
"""

__author__ = "Anders Logg (logg@simula.no) and Kristian B. Oelgaard (k.b.oelgaard@tudelft.nl)"
__date__ = "2007-02-05"
__copyright__ = "Copyright (C) 2007-2009 " + __author__
__license__  = "GNU GPL version 3 or any later version"

# UFL modules
from ufl.common import istr
from ufl.algorithms import preprocess, FormData
from ufl.algorithms import estimate_max_polynomial_degree
from ufl.algorithms import estimate_total_polynomial_degree

# FFC modules
from ffc.log import log, info, begin, end
from ffc.quadratureelement import default_quadrature_degree

def analyze_form(form, options):
    "Analyze form, returning preprocessed form and form data."

    begin("Compiler stage 1: Analyzing form")

    # Preprocess form
    if not form.is_preprocessed():
        form = preprocess(form)

    # Compute form data
    form_data = FormData(form)
    info(str(form_data))

    # Adjust cell and degree for elements when unspecified
    _adjust_elements(form_data)

    # Extract integral metadata
    form_data.metadata = _extract_metadata(form, options, form_data.elements)

    end()

    return form, form_data

def _adjust_elements(form_data):
    "Adjust cell and degree for elements when unspecified"

    # Extract common cell
    common_cell = form_data.cell
    if common_cell.domain() is None:
        error("Missing cell definition in form.")

    # Extract common degree
    common_degree = max([element.degree() for element in form_data.elements])
    if common_degree is None:
        common_degree = default_quadrature_degree

    # Set cell and degree if missing
    for element in form_data.elements:

        # Check if cell and degree need to be adjusted
        cell = element.cell()
        degree = element.degree()
        if degree is None:
            #info("Adjusting element degree from %s to %d" % (istr(degree), common_degree))
            log(30, "Adjusting element degree from %s to %d" % (istr(degree), common_degree))
            element.set_degree(common_degree)
        if cell.domain() is None:
            #info("Adjusting element cell from %s to %s." % (istr(cell), str(common_cell)))
            log(30, "Adjusting element cell from %s to %s." % (istr(cell), str(common_cell)))
            element.set_cell(common_cell)

def _extract_metadata(form, options, elements):
    "Check metadata for integral and return new integral with proper metadata."

    metadata = {}

    # Iterate over integrals
    for integral in form.integrals():

        # Set default values for metadata
        representation = options["representation"]
        quadrature_degree = options["quadrature_degree"]
        quadrature_rule = options["quadrature_rule"]

        if quadrature_rule is None:
            info("Quadrature rule: default")
        else:
            info("Quadrature rule: " + str(quadrature_rule))
        info("Quadrature order: " + str(quadrature_degree))

        # Get metadata for integral (if any)
        integral_metadata = integral.measure().metadata() or {}
        for (key, value) in integral_metadata.iteritems():
            if key == "ffc_representation":
                representation = integral_metadata["ffc_representation"]
            elif key == "quadrature_degree":
                quadrature_degree = integral_metadata["quadrature_degree"]
            elif key == "quadrature_rule":
                quadrature_rule = integral_metadata["quadrature_rule"]
            else:
                warning("Unrecognized option '%s' for integral metadata." % key)

        # Check metadata
        valid_representations = ["tensor", "quadrature", "auto"]
        if not representation in valid_representations:
            error("Unrecognized form representation '%s', must be one of %s.",
                  representation, ", ".join("'%s'" % r for r in valid_representations))
        if quadrature_degree != "auto":
            try:
                quadrature_degree = int(quadrature_degree)
                if not quadrature_degree >= 0:
                    error("Illegal quadrature order '%s' for integral, must be a nonnegative integer.",
                        str(quadrature_degree))
            except:
                error("Illegal quadrature order '%s' for integral, must be a nonnegative integer or 'auto'.",
                    str(quadrature_degree))

        # Automatically select metadata if "auto" is selected
        if representation == "auto":
            representation = _auto_select_representation(integral)
        if quadrature_degree == "auto":
            quadrature_degree = _auto_select_quadrature_degree(integral, representation, elements)
        log(30, "Integral quadrature degree is %d." % quadrature_degree)

        # No quadrature rules have been implemented yet
        if quadrature_rule:
            warning("No quadrature rules have been implemented yet, using the default from FIAT.")

        # Set metadata for integral
        metadata[integral] = {"quadrature_degree": quadrature_degree,
                              "ffc_representation": representation,
                              "quadrature_rule":quadrature_rule}

    return metadata

def _auto_select_representation(integral):
    "Automatically select the best representation for integral."

    # FIXME: Implement this
    info("Automatic selection of representation not implemented, defaulting to quadrature.")
    return "quadrature"

def _auto_select_quadrature_degree(integral, representation, elements):
    "Automatically select the appropriate quadrature degree for integral."

    # Estimate total degree of integrand
    degree = estimate_total_polynomial_degree(integral, default_quadrature_degree)

    # Use maximum quadrature element degree if any for quadrature representation
    if representation == "quadrature":
        #quadrature_elements = [e for e in elements if e.family() == "Quadrature"]
        #degree = max([degree] + [e.degree() for e in quadrature_elements])
        quadrature_degrees = [e.degree() for e in elements if e.family() == "Quadrature"]
        if quadrature_degrees != []:
            ffc_assert(min(quadrature_degrees) == max(quadrature_degrees), \
                       "All QuadratureElements in an integrand must have the same degree: %s" \
                       % str(quadrature_degrees))
            degree = quadrature_degrees[0]

    return degree
