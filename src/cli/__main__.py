# SPDX-FileCopyrightText: 2025-present Laurent LAPORTE <laurent.laporte.pro@gmail.com>
#
# SPDX-License-Identifier: MIT
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
