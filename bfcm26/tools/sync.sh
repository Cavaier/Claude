#!/bin/sh
# sync.sh "<commit message>" : copy blobmap into bfcm26/canvas, commit everything under bfcm26 + CLAUDE.md, push. Prints one line.
# It does NOT copy boards: copy the boards you changed (from the live canvas) into bfcm26/canvas/ yourself first, so stale scratch copies never overwrite newer ones.
S=${S:-/tmp/claude-0/-home-user-Claude/e5a7ae32-9047-5f38-90c5-952dcdd3ef9a/scratchpad}
R=/home/user/Claude; B=claude/focused-davinci-41clp5
cd $R && git pull -q origin $B 2>/dev/null
[ -f "$S/tools/blobmap.json" ] && cp $S/tools/blobmap.json $R/bfcm26/canvas/blobmap.json
git add -A bfcm26 CLAUDE.md
git diff --cached --quiet && { echo "sync: nothing to commit"; exit 0; }
git commit -qm "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01LtGMNmy7hV4kZNsS3Vsb6Q" && (git push -q origin $B || (git pull -q --rebase origin $B && git push -q origin $B)) && echo "sync: $(git log --oneline -1)"
