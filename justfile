test-quick:
    uv run --group dev pytest \
    --ignore=tests/test_large_vocab.py \
    --ignore=tests/test_speed.py

test:
    uv run --group dev pytest

serve-docs:
    uv run --group docs mkdocs serve

[confirm]
publish-docs:
    # make sure the remote exists
    git remote -v | grep deploy-doc > /dev/null || git remote add deploy-docs git@github.com:jitsi/jiwer.git
    git remote set-url deploy-docs git@github.com:jitsi/jiwer.git

    # push to deploy-docs remote and gh-pages branch
    uv run --group docs mkdocs gh-publish -r deploy-docs -b gh-pages
