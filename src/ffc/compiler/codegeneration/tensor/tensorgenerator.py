"Code generator for tensor representation"

__author__ = "Anders Logg (logg@simula.no)"
__date__ = "2004-11-03 -- 2007-06-11"
__copyright__ = "Copyright (C) 2004-2007 Anders Logg"
__license__  = "GNU GPL Version 2"

# Modified by Kristian B. Oelgaard 2007

# Python modules
from sets import Set

# FFC common modules
from ffc.common.constants import *

# FFC language modules
from ffc.compiler.language.index import *

# FFC code generation common modules
from ffc.compiler.codegeneration.common.codegenerator import *

# FFC format modules
from ffc.compiler.format.removeunused import *

class TensorGenerator(CodeGenerator):
    "Code generator for for tensor representation"

    def __init__(self):
        "Constructor"

        # Initialize common code generator
        CodeGenerator.__init__(self)

    def generate_cell_integral(self, form_representation, sub_domain, format):
        """Generate dictionary of code for cell integral from the given
        form representation according to the given format"""

        # Extract terms
        terms = form_representation.cell_tensor
        if len(terms) == 0:
            return None

        # Generate code for manipulating coefficients
#        code = self.__generate_coefficients(terms, format)

        # Generate code for geometry tensor
#        code += self.__generate_geometry_tensors(terms, format)

        # Generate code for sign changes
#        (sign_code, change_signs) = self.__generate_signs(terms, format)
#        code += sign_code
        
        # Generate code for element tensor(s)
#        code += [""] + [format["comment"]("Compute element tensor")]
#        code += self.__generate_element_tensor(terms, change_signs, format)

        # Generate code for sign changes
        (sign_code, change_signs) = self.__generate_signs(terms, format)

        # Generate element code + set of used geometry terms + set of used signs
        element_code, geo_set, sign_set = self.__generate_element_tensor(terms, change_signs, format)

        # Remove unused declarations
        sign_code = self.__remove_unused(sign_code, sign_set, format)

        # Generate geometry code + set of used coefficients + set of jacobi terms
        geo_code, coeff_set, trans_set = self.__generate_geometry_tensors(terms, geo_set, format)

        # FIXME: Get cell_shape in a more general way
        cell_shape = terms[0].monomial.basisfunctions[0].element.cell_shape()

        # Get Jacobian snippet
        jacobi_code = [format["generate jacobian"](cell_shape, Integral.CELL)]

        # Remove unused declarations
        code = self.__remove_unused(jacobi_code, trans_set, format)

        # Generate code for manipulating coefficients
        code += self.__generate_coefficients(terms, coeff_set, format)

        # Add geometry tensor declarations and sign code
        code += geo_code + sign_code

        # Add element code
        code += [""] + [format["comment"]("Compute element tensor")]
        code += element_code

        return {"tabulate_tensor": code, "members":""}

    def generate_exterior_facet_integral(self, form_representation, sub_domain, format):
        """Generate dictionary of code for exterior facet integral from the given
        form representation according to the given format"""

        # Extract terms
        terms = form_representation.exterior_facet_tensors
        if len(terms) == 0:
            return None

        # Generate code for manipulating coefficients (should be the same so pick first)
#        code = self.__generate_coefficients(terms[0], format)
        
        # Generate code for geometry tensor (should be the same so pick first)
#        code += self.__generate_geometry_tensors(terms[0], format)

        # Generate code for element tensor(s)
#        code += [""] + [format["comment"]("Compute element tensor for all facets")]

        num_facets = len(terms)
        cases = [None for i in range(num_facets)]
#        for i in range(num_facets):
#            cases[i] = self.__generate_element_tensor(terms[i], False, format)

        # Generate element code + set of used geometry terms
        geo_set = Set()
        for i in range(num_facets):
            case, g_set, s_set = self.__generate_element_tensor(terms[i], False, format)
            cases[i] = case
            geo_set = geo_set | g_set

        # Generate code for geometry tensor (should be the same so pick first)
        # Generate geometry code + set of used coefficients + set of jacobi terms
        geo_code, coeff_set, trans_set = self.__generate_geometry_tensors(terms[0], geo_set, format)

        # FIXME: Get cell_shape in a more general way
        cell_shape = terms[0][0].monomial.basisfunctions[0].element.cell_shape()

        # Get Jacobian snippet
        jacobi_code = [format["generate jacobian"](cell_shape, Integral.EXTERIOR_FACET)]

        # Remove unused declarations
        code = self.__remove_unused(jacobi_code, trans_set, format)

        # Generate code for manipulating coefficients (should be the same so pick first)
        code += self.__generate_coefficients(terms[0], coeff_set, format)

        # Add geometry tensor declarations
        code += geo_code

        # Add element code
        code += [""] + [format["comment"]("Compute element tensor for all facets")]

        return {"tabulate_tensor": (code, cases), "members":""}
    
    def generate_interior_facet_integral(self, form_representation, sub_domain, format):
        """Generate dictionary of code for interior facet integral from the given
        form representation according to the given format"""

        # Extract terms
        terms = form_representation.interior_facet_tensors
        if len(terms) == 0:
            return None

        # Generate code for manipulating coefficients (should be the same so pick first)
#        code = self.__generate_coefficients(terms[0][0], format)
        
        # Generate code for geometry tensor (should be the same so pick first)
#        code += self.__generate_geometry_tensors(terms[0][0], format)

        # Generate code for element tensor(s)
#        code += [""] + [format["comment"]("Compute element tensor for all facet-facet combinations")]
        num_facets = len(terms)
        cases = [[None for j in range(num_facets)] for i in range(num_facets)]
#        for i in range(num_facets):
#            for j in range(num_facets):
#                cases[i][j] = self.__generate_element_tensor(terms[i][j], False, format)

        # Generate element code + set of used geometry terms
        geo_set = Set()
        for i in range(num_facets):
            for j in range(num_facets):
                case, g_set, s_set = self.__generate_element_tensor(terms[i][j], False, format)
                cases[i][j] = case
                geo_set = geo_set | g_set

        # Generate code for geometry tensor (should be the same so pick first)
        # Generate geometry code + set of used coefficients + set of jacobi terms
        geo_code, coeff_set, trans_set = self.__generate_geometry_tensors(terms[0][0], geo_set, format)

        # FIXME: Get cell_shape in a more general way
        cell_shape = terms[0][0][0].monomial.basisfunctions[0].element.cell_shape()

        # Get Jacobian snippet
        jacobi_code = [format["generate jacobian"](cell_shape, Integral.INTERIOR_FACET)]

        # Remove unused declarations
        code = self.__remove_unused(jacobi_code, trans_set, format)

        # Generate code for manipulating coefficients (should be the same so pick first)
        code += self.__generate_coefficients(terms[0][0], coeff_set, format)

        # Add geometry tensor declarations
        code += geo_code

        # Add element code
        code += [""] + [format["comment"]("Compute element tensor for all facet-facet combinations")]

        return {"tabulate_tensor": (code, cases), "members":""}

    def __generate_coefficients(self, terms, coeff_set, format):
        "Generate code for manipulating coefficients"

        # Generate code as a list of declarations
        code = []

        # Add comment
        code += [format["comment"]("Compute coefficients")]

        # A coefficient is identified by 4 numbers:
        #
        #   0 - the number of the function
        #   1 - the position of the (factored) monomial it appears in
        #   2 - the position of the coefficient inside the monomial
        #   3 - the position of the expansion coefficient

        # Iterate over all terms
        j = 0

        for term in terms:
            for G in term.G:
                for k in range(len(G.coefficients)):
                    coefficient = G.coefficients[k]
                    if term.monomial.integral.type == Integral.INTERIOR_FACET:
                        space_dimension = 2*len(coefficient.index.range)
                    else:
                        space_dimension = len(coefficient.index.range)
                    for l in range(space_dimension):
                        # If coefficient is not used don't declare it
                        if not format["modified coefficient access"](coefficient.n0.index, j, k, l) in coeff_set:
                            continue
                        name = format["modified coefficient declaration"](coefficient.n0.index, j, k, l)
                        value = format["coefficient"](coefficient.n0.index, l)
                        for l in range(len(coefficient.ops)):
                            op = coefficient.ops[len(coefficient.ops) - 1 - l]
                            if op == Operators.INVERSE:
                                value = format["inverse"](value)
                            elif op == Operators.ABS:
                                value = format["absolute value"](value)
                            elif op == Operators.SQRT:
                                value = format["sqrt"](value)
                        code += [(name, value)]
                j += 1

        # Don't add code if there are no coefficients
        if len(code) == 1:
            return []

        # Add newline
        code += [""]

        return code

    def __generate_geometry_tensors(self, terms, geo_set, format):
        "Generate list of declarations for computation of geometry tensors"

        # Generate code as a list of declarations
        code = []    
        
        # Add comment
        code += [format["comment"]("Compute geometry tensors")]

        # Iterate over all terms
        j = 0
        coeff_set = Set()
        trans_set = Set()
        for i in range(len(terms)):

            term = terms[i]

            # Get list of secondary indices (should be the same so pick first)
            aindices = terms[i].G[0].a.indices

            # Iterate over secondary indices
            for a in aindices:

                # Skip code generation if term is not used
                if not format["geometry tensor access"](i,a) in geo_set:
                    continue

                # Compute factorized values
                values = []
                jj = j
                for G in term.G:
                    val, c_set, t_set = self.__generate_entry(G, a, jj, format)
                    values += [val]
                    coeff_set = coeff_set | c_set
                    trans_set = trans_set | t_set
                    jj += 1

                # Sum factorized values
                name = format["geometry tensor declaration"](i, a)
                value = format["add"](values)

                # Multiply with determinant factor
                det = pick_first([G.determinant for G in term.G])
                value = self.__multiply_value_by_det(value, det, format, len(values) > 1)

                # Add determinant to transformation set
                if det:
                    trans_set.add(format["power"](format["determinant"], det))

                # Add declaration
                code += [(name, value)]

            j += len(term.G)

        # Add scale factor
        trans_set.add(format["scale factor"])

        return (code, coeff_set, trans_set)

    def __generate_element_tensor(self, terms, sign_changes, format):
        "Generate list of declaration for computation of element tensor"

        # Generate code as a list of declarations
        code = []    
    
        # Get list of primary indices (should be the same so pick first)
        iindices = terms[0].A0.i.indices

        # Prefetch formats to speed up code generation
        format_element_tensor  = format["element tensor"]
        format_geometry_tensor = format["geometry tensor access"]
        format_add             = format["add"]
        format_subtract        = format["subtract"]
        format_multiply        = format["multiply"]
        format_floating_point  = format["floating point"]
        format_epsilon         = format["epsilon"]

        # Generate code for geometry tensor entries
        gk_tensor = [ ( [(format_geometry_tensor(j, a), a) for a in terms[j].A0.a.indices], j) for j in range(len(terms)) ]

        # Generate code for computing the element tensor
        k = 0
        num_dropped = 0
        num_ops = 0
        zero = format_floating_point(0.0)
        sign_set = Set()
        geo_set = Set()
        for i in iindices:
            name = format_element_tensor(i, k)
            value = None
            for (gka, j) in gk_tensor:
                A0 = terms[j].A0
                for (gk, a) in gka:
                    a0 = A0.A0[tuple(i + a)]
                    if abs(a0) > format_epsilon:
                        if value and a0 < 0.0:
                            value = format_subtract([value, format_multiply([format_floating_point(-a0), gk])])
                            geo_set.add(gk)
                        elif value:
                            value = format_add([value, format_multiply([format_floating_point(a0), gk])])
                            geo_set.add(gk)
                        else:
                            value = format_multiply([format_floating_point(a0), gk])
                            geo_set.add(gk)
                        num_ops += 1
                    else:
                        num_dropped += 1

            # Add sign changes as appropriate.
            if sign_changes:
                value, signs = self.__add_sign(value, 0, i, format)
                sign_set = sign_set | signs
            value = value or zero
            code += [(name, value)]
            k += 1

        return (code, geo_set, sign_set)

    def __generate_entry(self, G, a, i, format):
        "Generate code for the value of entry a of geometry tensor G"

        coeff_set = Set()
        trans_set = Set()

        # Compute product of factors outside sum
        factors = []
        for j in range(len(G.coefficients)):
            c = G.coefficients[j]
            if not c.index.type == Index.AUXILIARY_G:
                coefficient = format["modified coefficient access"](c.n1.index, i, j, c.index([], a, [], []))
                coeff_set.add(coefficient)
                factors += [coefficient]
            
        for t in G.transforms:
            if not (t.index0.type == Index.AUXILIARY_G or  t.index1.type == Index.AUXILIARY_G):
                trans = format["transform"](t.type, t.index0([], a, [], []), \
                                                        t.index1([], a, [], []), \
                                                        t.restriction)
                factors += [trans]
                trans_set.add(trans)

        monomial = format["multiply"](factors)
        if monomial: f0 = [monomial]
        else: f0 = []
    
        # Compute sum of monomials inside sum
        terms = []
        for b in G.b.indices:
            factors = []
            for j in range(len(G.coefficients)):
                c = G.coefficients[j]
                if c.index.type == Index.AUXILIARY_G:
                    coefficient = format["modified coefficient access"](c.n1.index, i, j, c.index([], a, [], b))
                    coeff_set.add(coefficient)
                    factors += [coefficient]
            for t in G.transforms:
                if t.index0.type == Index.AUXILIARY_G or t.index1.type == Index.AUXILIARY_G:
                    trans = format["transform"](t.type, t.index0([], a, [], b), \
                                                            t.index1([], a, [], b), \
                                                            t.restriction)
                    factors += [trans]
                    trans_set.add(trans)
            terms += [format["multiply"](factors)]

        sum = format["add"](terms)
        if sum: sum = format["grouping"](sum)
        if sum: f1 = [sum]
        else: f1 = []

        fs = f0 + f1
        if not fs: fs = ["1.0"]

        # Compute product of all factors
        return (format["multiply"](fs), coeff_set, trans_set)

    def __generate_signs(self, terms, format):
        "Generate list of declarations for computation of signs"
        code = []
        computed = {}
        for j in range(len(terms)):
            monomial = terms[j].monomial
            # Inspect each basis function (identified by its index)
            # and check whether sign changes are relevant.
            for basisfunction in monomial.basisfunctions:
                index = basisfunction.index
                if not str(index) in computed:
                    necessary = False
                    element = basisfunction.element
                    declarations = []
                    dof_entities = DofMap(element).dof_entities();

                    # Go through the topological entities associated
                    # with each basis function/dof. If the element is
                    # a piola mapped element and the basis function is
                    # associated with an edge, we calculate the
                    # possible sign change.
                    for no in dof_entities:
                        (entity, entity_no) = dof_entities[no]
                        name = format["sign tensor"](j, index.index, no)
                        if entity == 1 and element.space_mapping(no) == Mapping.PIOLA:
                            necessary = True
                            value = format["facet sign"](entity_no)
                            # If the sign of this edge already has
                            # been computed, refer to that entry instead.
                            if value in computed:
                                value = computed[value]
                            else:
                                computed[value] = name
                        else:
                            value = "1"

                        # Add to declarations
                        declarations += [(format["sign tensor declaration"](name), value)]    

                    # Add declarations for this basis function to the code
                    code += declarations
                    computed[str(index)] = True
                    
        if necessary:
            code.insert(0, format["comment"]("Compute signs"))
            code.insert(0, format["snippet facet signs"](2))
            return (code, True)
        else:
            return ([], False) # Return [] is the case of no sign changes...)

    def __add_sign(self, value, j, i, format):

        sign_set = Set()
        if value:
            value = format["grouping"](value)
            for k in range(len(i)):
                value = format["multiply"]([format["sign tensor"](j, k, i[k]), value])
                sign_set.add(format["sign tensor"](j, k, i[k]))
        return (value, sign_set)

    def __multiply_value_by_det(self, value, det, format, is_sum):
        if det: d0 = [format["power"](format["determinant"], det)]
        else: d0 = []
        if value == "1.0":
            v = []
        elif is_sum:
            v = [format["grouping"](value)]
        else:
            v = [value]
        return format["multiply"](d0 + [format["scale factor"]] + v)

    def __remove_unused(self, code, set, format):

        if code:
            # Fixme: Following lines are from ufcformat.py __generate_body()
            lines = []
            for line in code:
                if isinstance(line, tuple):
                    lines += ["%s = %s;" % line]
                else:
                    lines += ["%s" % line]

            # Generate auxiliary code line that uses all members of the set (to trick remove_unused)
            line_set = format["add equal"]("A", format["multiply"](set))
            lines += [line_set]

            # Remove unused Jacobi declarations
            code = remove_unused("\n".join(lines))

            # Delete auxiliary line
            code = code.replace("\n" + line_set, "")

            return code.split("\n")
        else:
            return code
