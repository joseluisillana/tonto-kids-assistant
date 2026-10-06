"""These tests run inside task containers and verify the effective mount boundary."""

from pathlib import Path
import os

import pytest


@pytest.mark.skipif(not Path('/.dockerenv').exists(), reason='Effective mount check requires Docker')
def test_task_container_excludes_repository_secrets():
    root = Path('/app')
    for name in ('.env', '.env.private', '.git', 'secrets', 'docs', 'exports'):
        assert not (root / name).exists()
    assert not list(root.glob('.env.*'))
    for name in ('backend', 'client', 'shared', 'tests', 'scripts', 'tonto.sh',
                 'docker-compose.yml', 'docker-compose.tasks.yml', 'requirements-dev.txt'):
        assert (root / name).exists()
    for name in ('backend', 'client', 'shared', 'tests', 'scripts'):
        assert not os.access(root / name, os.W_OK)
    assert os.access(root / '.cache/pytest-fixtures', os.W_OK)


def test_ui_context_is_dockerfile_only():
    root = Path(__file__).resolve().parents[1]
    assert (root / 'client/.dockerignore').read_text().splitlines()[1:] == ['**', '!Dockerfile.ui']
    for name in ('docker-compose.yml', 'docker-compose.tasks.yml'):
        text = (root / name).read_text()
        assert 'context: ./client\n      dockerfile: Dockerfile.ui' in text
        assert '- .:/app' not in text
        assert '- ./web:/app/web' not in text
