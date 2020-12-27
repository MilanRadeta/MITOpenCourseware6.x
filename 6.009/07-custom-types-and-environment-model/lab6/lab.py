#!/usr/bin/env python3
"""6.009 Lab 6 -- Boolean satisfiability solving"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS

def subsets(lst, n): 
      
    if n == 0: 
        return [[]] 
      
    l =[] 
    for i in range(0, len(lst)): 
          
        m = lst[i] 
        remLst = lst[i + 1:] 
          
        for p in subsets(remLst, n-1): 
            l.append([m]+p) 
              
    return l

def satisfying_assignment(formula, res=None):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """
    formula = sorted(formula, key=lambda clause: len(clause))
    if res is None:
        res = {}
    i = 0
    while i < len(formula):
        clause = formula[i]
        if len(clause) == 1:
            var, lit = clause[0]
            if var in res and res[var] != lit:
                return None
            res[var] = lit
            formula.remove(clause)
            continue
        else:
            skip = False
            for var, lit in clause:
                if var in res:
                    if res[var] == lit:
                        formula.remove(clause)
                    else:
                        formula[i] = clause[:]
                        formula[i].remove((var,lit))
                    skip = True
                    break
                    
            if skip:
                continue
            
        i += 1
    if len(formula) == 0:
        return {key: val for key, val in res.items() if val is not None}

    for clause in formula:
        for var, lit in clause:
            if var not in res:
                for lit in (lit, not lit):
                    res[var] = lit
                    subres = satisfying_assignment(formula, res.copy())
                    if subres is not None:
                        return subres
                res[var] = None
        
    return None


def boolify_scheduling_problem(student_preferences, session_capacities):
    """
    Convert a quiz-room-scheduling problem into a Boolean formula.

    student_preferences: a dictionary mapping a student name (string) to a set
                         of session names (strings) that work for that student
    session_capacities: a dictionary mapping each session name to a positive
                        integer for how many students can fit in that session

    Returns: a CNF formula encoding the scheduling problem, as per the
             lab write-up
    We assume no student or session names contain underscores.
    """
    cnf = []

    for student, rooms in student_preferences.items():
        cnf += [[('%s_%s' % (student, room), True) for room in rooms]]
        for room in rooms:
            for other in rooms:
                if other != room:
                    cnf += [[('%s_%s' % (student, room), False), ('%s_%s' % (student, other), False)]]

    for room, capacity in session_capacities.items():
        students = [student for student, rooms in student_preferences.items() if room in rooms]
        if capacity < len(students):
            in_students_lists = subsets(students, capacity)
            for l in in_students_lists:
                for student in students:
                    if student not in l:
                        cnf += [[('%s_%s' % (s, room), False) for s in l] + [('%s_%s' % (student, room), False)]]
                    

    return cnf


if __name__ == '__main__':
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)
