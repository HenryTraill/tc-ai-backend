#!/usr/bin/env python3
"""Development server script for TutorCruncher API"""

import uvicorn

from app.core.config import settings

if __name__ == '__main__':
    uvicorn.run('app.main:app', host=settings.api_host, port=settings.api_port, reload=True, log_level='info')
