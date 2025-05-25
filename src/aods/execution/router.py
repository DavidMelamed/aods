"""Route opportunities to executors."""
from __future__ import annotations

import os
from typing import Dict, Callable

from .google_ads import launch_keyword

EXECUTION_MODE = os.getenv('EXECUTION_MODE', 'DRY')

ROUTES: Dict[str, Callable] = {
    'keyword': launch_keyword,
}


def execute(opportunity: dict) -> dict:
    if EXECUTION_MODE.upper() == 'DRY':
        return {'status': 'dry-run', **opportunity}
    exec_fn = ROUTES.get(opportunity.get('type'))
    if not exec_fn:
        raise ValueError('unknown type')
    return exec_fn(**opportunity)
