#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2012-2013 Raphaël Barrois
# This code is distributed under the LGPLv3 License.

import unittest

from djadmin_export import utils


class UtilsTestCase(unittest.TestCase):
    def test_asciify(self):
        self.assertEqual('foo', utils.asciify('foo'))
        self.assertEqual('bar', utils.asciify(u"bàr"))
        self.assertEqual('Eeucna', utils.asciify(u'Ëéüçñøá'))

    def test_slugify(self):
        self.assertEqual(u'foo', utils.slugify(u"  F,ôö  "))
        self.assertEqual(u'ba-bar', utils.slugify(u" Bà,'      bär"))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
