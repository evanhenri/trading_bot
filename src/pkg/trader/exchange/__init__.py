import logging
import sys

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler(sys.stdout))

from .gemini import Gemini
from .poloniex import Poloniex
