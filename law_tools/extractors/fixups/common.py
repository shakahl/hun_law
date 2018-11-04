# Copyright 2018 Alex Badics <admin@stickman.hu>
#
# This file is part of Law-tools.
#
# Law-tools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Law-tools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Law-tools.  If not, see <https://www.gnu.org/licenses/>.


# The whole module is a bunch of fixups to existing Acts, that aren't
# well-formed enough to be parsed by the parser out-of-the-box

from law_tools.utils import IndentedLine, EMPTY_LINE
all_fixups = {}

def add_fixup(law_id, fixup_cb):
    global all_fixups
    if law_id in all_fixups:
        all_fixups[law_id].append(fixup_cb)
    else:
        all_fixups[law_id] = [fixup_cb]

def do_all_fixups(law_id, body):
    global all_fixups
    if law_id not in all_fixups:
        return body
    for fixup in all_fixups[law_id]:
        try:
            body  = fixup(body)
        except Exception as e:
            raise ValueError(
                "Fixup {} could not be done for {}: {}".format(fixup.__name__, law_id, e)
            ) from e
    return body


def add_empty_line_after(needle):
    def empty_line_adder(body):
        result = []
        needle_count = 0
        for l in body:
            result.append(l)
            if l.content == needle:
                result.append(EMPTY_LINE)
                needle_count = needle_count + 1
        if needle_count == 0:
            raise ValueError("Text '{}' not found in body".format(needle))
        if needle_count != 1:
            raise ValueError("Text '{}' found too many times in body: {}".format(needle, needle_count))
        return result
    return empty_line_adder


def replace_line_content(needle, replacement):
    def line_content_replacer(body):
        result = []
        needle_count = 0
        for l in body:
            if l.content != needle:
                result.append(l)
            else:
                result.append(IndentedLine(replacement, l.indent))
                needle_count = needle_count + 1
        if needle_count == 0:
            raise ValueError("Text '{}' not found in body".format(needle))
        if needle_count != 1:
            raise ValueError("Text '{}' found too many times in body: {}".format(needle, needle_count))
        return result
    return line_content_replacer
