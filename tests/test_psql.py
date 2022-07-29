# -*- coding: utf-8 -*-

import os
import pytest
from typing import Optional
import sqlalchemy as sa


class TestCase:
    engine: Optional[sa.engine.Engine] = None

    @classmethod
    def setup_class(cls):
        conn_str = (
            f"postgresql+pg8000://postgres:mypassword@localhost:5432/postgres"
        )
        cls.engine = sa.engine.create_engine(conn_str)

    def test(self):
        row = self.engine.execute("SELECT 999;").fetchone()
        assert row[0] == 999


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
