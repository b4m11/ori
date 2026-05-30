#!/usr/bin/env bash
# setup_sudoers.sh (run this as root!)

set -euo pipefail

useradd -m -G sudo -s /bin/zsh syca

cat >/etc/sudoers.d/ori <<'EOF'
syca ALL=(syca) NOPASSWD: ALL
EOF

chmod 440 /etc/sudoers.d/ori
visudo -cf /etc/sudoers.d/ori
