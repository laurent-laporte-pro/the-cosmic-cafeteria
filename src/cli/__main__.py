# SPDX-FileCopyrightText: 2025-present Laurent LAPORTE <laurent.laporte.pro@gmail.com>
#
# SPDX-License-Identifier: MIT
import sys

if __name__ == "__main__":
    from cli.app import main_cmd

    sys.exit(main_cmd())
