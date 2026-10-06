"""Exercise the real export script against public fixtures, never real secrets."""

from pathlib import Path
import shutil
import subprocess
import os

import pytest


@pytest.fixture
def export_repo(tmp_path):
    root = tmp_path / 'repo'
    for name in ('scripts', 'docs', 'specs', 'web', 'exports/notebooklm'):
        (root / name).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path(__file__).resolve().parents[1] / 'scripts/export-docs-for-notebooklm.sh',
                    root / 'scripts/export-docs-for-notebooklm.sh')
    for name in ('README.md', 'AGENTS.md', 'docs/example.md', 'specs/example.md', 'web/README.md'):
        (root / name).write_text(f'Public fixture: {name}\n')
    (root / 'exports/notebooklm/previous.txt').write_text('previous export')
    return root


def run_export(root, destination=None, env=None):
    return subprocess.run(['bash', str(root / 'scripts/export-docs-for-notebooklm.sh'),
                           *([] if destination is None else [str(destination)])],
                          capture_output=True, text=True, env=env)


@pytest.mark.parametrize('destination', [None, 'exports/custom', 'exports/../exports/normalized'])
def test_export_preserves_format_and_sources(export_repo, destination):
    result = run_export(export_repo, destination)
    assert result.returncode == 0
    output = export_repo / (destination or 'exports/notebooklm')
    combined = (output / 'NOTEBOOKLM_COMBINED.md').read_text()
    for name in ('README.md', 'AGENTS.md', 'docs/example.md', 'specs/example.md', 'web/README.md'):
        source = (export_repo / name).read_text()
        assert (output / name.replace('/', '__')).read_text() == source
        assert f'## Source: {name}\n\n{source}' in combined
        assert name.replace('/', '__') in (output / 'INDEX.md').read_text()
    assert not (output / 'previous.txt').exists()
    assert not list(output.parent.glob('.notebooklm-*'))


@pytest.mark.parametrize('destination', ['.', 'exports', 'docs', 'specs', 'web', '.git',
                                       'exports/../../outside', '../repo-sibling/output'])
def test_export_rejects_dangerous_destinations(export_repo, destination):
    before = (export_repo / 'docs/example.md').read_text()
    result = run_export(export_repo, destination)
    assert result.returncode != 0
    assert (export_repo / 'docs/example.md').read_text() == before
    assert (export_repo / 'exports/notebooklm/previous.txt').exists()


@pytest.mark.parametrize('kind', ['file', 'directory', 'root', 'broken', 'hardlink', 'protected'])
def test_export_rejects_source_aliases_without_leaking(export_repo, kind):
    secret = export_repo / '.env'
    canary = 'invented-export-canary'
    secret.write_text(canary)
    if kind == 'file':
        (export_repo / 'docs/alias.md').symlink_to(secret)
    elif kind == 'directory':
        (export_repo / 'docs/alias').symlink_to(export_repo, target_is_directory=True)
    elif kind == 'root':
        shutil.rmtree(export_repo / 'specs')
        (export_repo / 'specs').symlink_to(export_repo / 'docs', target_is_directory=True)
    elif kind == 'broken':
        (export_repo / 'docs/alias.md').symlink_to(export_repo / 'missing')
    elif kind == 'hardlink':
        (export_repo / 'docs/alias.md').hardlink_to(secret)
    else:
        (export_repo / 'docs/credentials.private.md').write_text(canary)
    result = run_export(export_repo)
    output = export_repo / 'exports/notebooklm'
    if canary in result.stdout + result.stderr + ''.join(p.read_text() for p in output.iterdir()):
        pytest.fail('Exporter exposed a canary', pytrace=False)
    assert result.returncode != 0
    assert (output / 'previous.txt').read_text() == 'previous export'


@pytest.mark.parametrize('position', ['parent', 'destination', 'ancestor', 'broken'])
def test_export_rejects_destination_links(export_repo, position):
    outside = export_repo.parent / 'outside'
    outside.mkdir()
    sentinel = outside / 'keep'
    sentinel.write_text('keep')
    if position == 'parent':
        shutil.rmtree(export_repo / 'exports')
        (export_repo / 'exports').symlink_to(outside, target_is_directory=True)
    elif position == 'destination':
        shutil.rmtree(export_repo / 'exports/notebooklm')
        (export_repo / 'exports/notebooklm').symlink_to(outside, target_is_directory=True)
    elif position == 'ancestor':
        (export_repo / 'exports/link').symlink_to(outside, target_is_directory=True)
    else:
        (export_repo / 'exports/link').symlink_to(outside / 'missing')
    result = run_export(export_repo, 'exports/link/output' if position in {'ancestor', 'broken'} else None)
    assert result.returncode != 0
    assert sentinel.read_text() == 'keep'


def test_export_copy_failure_keeps_previous_output_and_hides_errors(export_repo):
    bin_dir = export_repo / 'bin'
    bin_dir.mkdir()
    cp = bin_dir / 'cp'
    cp.write_text('#!/bin/bash\necho "$FAKE_ERROR" >&2\nexit 31\n')
    cp.chmod(0o755)
    canary = 'invented-io-canary'
    result = run_export(export_repo, env={**os.environ, 'PATH': f'{bin_dir}:{os.environ["PATH"]}',
                                          'FAKE_ERROR': canary})
    if canary in result.stdout + result.stderr:
        pytest.fail('Exporter exposed raw IO diagnostics', pytrace=False)
    assert result.returncode != 0
    assert (export_repo / 'exports/notebooklm/previous.txt').exists()
    assert not list((export_repo / 'exports').glob('.notebooklm-*'))
