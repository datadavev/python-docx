# encoding: utf-8

"""
Test suite for pptx.oxml.__init__.py module, primarily XML parser-related.
"""

from __future__ import print_function, unicode_literals

import pytest

from lxml import etree

from docx.oxml import oxml_parser, parse_xml, register_custom_element_class
from docx.oxml.shared import OxmlBaseElement


class DescribeOxmlParser(object):

    def it_strips_whitespace_between_elements(self, whitespace_fixture):
        pretty_xml_text, stripped_xml_text = whitespace_fixture
        element = etree.fromstring(pretty_xml_text, oxml_parser)
        xml_text = etree.tostring(element, encoding='unicode')
        assert xml_text == stripped_xml_text

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def whitespace_fixture(self):
        pretty_xml_text = (
            '<foø>\n'
            '  <bår>text</bår>\n'
            '</foø>\n'
        )
        stripped_xml_text = '<foø><bår>text</bår></foø>'
        return pretty_xml_text, stripped_xml_text


class DescribeParseXml(object):

    def it_accepts_bytes_and_assumes_utf8_encoding(self, xml_bytes):
        parse_xml(xml_bytes)

    def it_accepts_unicode_providing_there_is_no_encoding_declaration(self):
        non_enc_decl = '<?xml version="1.0" standalone="yes"?>'
        enc_decl = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        xml_body = '<foo><bar>føøbår</bar></foo>'
        # unicode body by itself doesn't raise
        parse_xml(xml_body)
        # adding XML decl without encoding attr doesn't raise either
        xml_text = '%s\n%s' % (non_enc_decl, xml_body)
        parse_xml(xml_text)
        # but adding encoding in the declaration raises ValueError
        xml_text = '%s\n%s' % (enc_decl, xml_body)
        with pytest.raises(ValueError):
            parse_xml(xml_text)

    def it_uses_registered_element_classes(self, xml_bytes):
        register_custom_element_class('a:foo', CustElmCls)
        element = parse_xml(xml_bytes)
        assert isinstance(element, CustElmCls)

    # fixture components ---------------------------------------------

    @pytest.fixture
    def xml_bytes(self):
        return (
            '<a:foo xmlns:a="http://schemas.openxmlformats.org/drawingml/200'
            '6/main">\n'
            '  <a:bar>foøbår</a:bar>\n'
            '</a:foo>\n'
        ).encode('utf-8')


# ===========================================================================
# static fixture
# ===========================================================================

class CustElmCls(OxmlBaseElement):
    pass