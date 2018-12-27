# Copyright 2018 Alex Badics <admin@stickman.hu>
#
# This file is part of Hun-Law.
#
# Hun-Law is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hun-Law is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hun-Law.  If not, see <https://www.gnu.org/licenses/>.

from hun_law.parsers.grammatical_analyzer import GrammaticalAnalyzer
from hun_law.structure import Reference, MutableReference


import pytest


def ref(act=None, article=None, paragraph=None, point=None, subpoint=None):
    return Reference(MutableReference(act, article, paragraph, point, subpoint))


CASES = [
    (
        "A hegyközségekről szóló 2012. évi CCXIX. törvény (a továbbiakban: Hktv.) 28. §-a helyébe a következő rendelkezés lép:",
        "                        [                      ]                         <     >                                     ",
        [ref("2012. évi CCXIX. törvény", '28')],
        ["2012. évi CCXIX. törvény", ],
    ),
    (
        # Test that quoted references are not parsed
        "Az Flt. 30. § (1) bekezdés a) pontjában az „a 25. § (1) bekezdésének c)–d) pontjában” szövegrész helyébe az „a 25. § (1) bekezdésének d) pontjában” szöveg lép.",
        "   [  ] <                             >                                                                                                                        ",
        [ref("Flt.", "30", '1', 'a'), ],
        ["Flt.", ],
    ),
    (
        "Az 1–30. §, a 31. § (1) és (3)−(5) bekezdése, a 32–34. §, a 35. § (1) és (3)–(5) bekezdése, a 36. §, a 37. § "
        "(1) és (3)–(5) bekezdése, a 38. §, a 39. § (1) és (3)–(5) bekezdése, a 40–59. §, a 60. § (1) bekezdése, a 61. § (1), (2) "
        "és (7) bekezdése, 62–66. §, a 67. § (5) bekezdés a)–d) és g) pontja, a 68. § (1)–(3), (10) és (12)–(15) bekezdése, "
        "(17) bekezdés 1., 2., 4., 6–8., 10–13., 15., 16., 18–20. és 25. pontja, a 69–76. §, a 77. § (3) és (4) bekezdése, a 78–82. §, "
        "a 181. §, a 182. §, a 192. § a)–b) pontja, valamint d)–n) pontja és a 193. § 2014. március 15-én lép hatályba.",
        None,
        None,
        None,
    ),
]


@pytest.fixture(scope="module")
def analyzer():
    return GrammaticalAnalyzer()


@pytest.mark.parametrize("s,positions,refs,act_refs", CASES)
def test_parse_results_are_stable(analyzer, s, positions, refs, act_refs):
    first_result = analyzer.analyze(s)
    for i in range(3):
        other_result = analyzer.analyze(s)
        assert first_result == other_result, ("Parsing always yields  the same result", case)


@pytest.mark.parametrize("s,positions,refs,act_refs", CASES)
def test_parse_results(analyzer, s, positions, refs, act_refs):
    if refs is None:
        return
    parsed = analyzer.analyze(s)
    parsed_refs = []
    parsed_act_refs = []
    parsed_pos_string = [" "] * len(s)
    for ref, start, stop in parsed.get_references():
        parsed_pos_string[start] = '<'
        parsed_pos_string[stop] = '>'
        parsed_refs.append(ref)
    for act_ref, start, stop in parsed.get_act_references():
        parsed_pos_string[start] = '['
        parsed_pos_string[stop] = ']'
        parsed_act_refs.append(act_ref)
    parsed_pos_string = "".join(parsed_pos_string)
    assert refs == parsed_refs
    assert act_refs == parsed_act_refs
    if positions is not None:
        assert positions == parsed_pos_string
