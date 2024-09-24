from nominatim_data_analyser.database.connection import connect


def test_connect(dsn) -> None:
    with connect(dsn) as conn:
        assert conn.status == 1
