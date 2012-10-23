# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois
# This code is distributed under the LGPLv3 License.

import re
import unicodedata

from django.utils.safestring import mark_safe


def asciify(unistr):
    """Returns an ascii string, converting accented chars to normal ones.

    Unconvertible chars are simply removed.

    Example:
        >>> asciify(u'Ééüçñøà')
            Eeucna
    """
    return unicodedata.normalize('NFKD', unicode(unistr)).encode('ascii', 'ignore')


def slugify(value):
    """Normalizes a string for use in a slug-like manner.

    Performs the following transformations:
    - Normalizes unicode chars
    - Converts everything to lowercase
    - Removes non alphanumeric chars
    - Replaces spaces with hyphens
    """
    # Normalize
    value = asciify(value)
    # Lowercase
    value = value.strip().lower()
    # Purge non-alphanum or space
    value = re.sub('[^\w\s-]', '', value)
    return mark_safe(unicode(re.sub('[-\s]+', '-', value)))
