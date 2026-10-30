import os
from datetime import datetime

import mysql.connector
import pytest

from ping_collector import save_ping


@pytest.fixture
def db_connection():
    # 沒有明確啟用時，不執行資料庫整合測試
    if os.getenv("RUN_DB_INTEGRATION_TESTS") != "1":
        pytest.skip("Database integration tests are disabled")

    # 安全檢查：只能連接指定的測試資料庫
    db_name = os.environ["TEST_DB_NAME"]    # 不存在時會拋出 KeyError

    if db_name != "network_monitor_test":
        pytest.fail("Integration tests must use network_monitor_test")

    # 建立連線
    connection = mysql.connector.connect(
        host=os.environ["TEST_DB_HOST"],
        port=int(os.getenv("TEST_DB_PORT", "3306")),
        user=os.environ["TEST_DB_USER"],
        password=os.environ["TEST_DB_PASSWORD"],
        database=db_name,
    )

    try:
        # 把連線提供給測試函式
        yield connection
    finally:
        # 測試結束後關閉連線
        connection.close()



@pytest.mark.integration
def test_save_ping_to_mysql(db_connection):
    test_time = datetime.now()
    test_latency = 12.5

    ping_id = None

    try:
        # 1. 寫入資料，取得新增的 ID
        ping_id = save_ping(
            db_connection,
            test_time,
            test_latency
        )

        # 2. 用 ID 查詢資料
        cursor = db_connection.cursor()

        try:
            cursor.execute(
                """
                SELECT latency_ms
                FROM ping_records
                WHERE id = %s
                """,
                (ping_id,)
            )

            result = cursor.fetchone()

            # 3. 驗證資料
            assert result is not None
            assert result[0] == pytest.approx(test_latency)

        finally:
            cursor.close()

    finally:
        # 4. 刪除本次測試新增的資料
        if ping_id is not None:
            cursor = db_connection.cursor()
            try:
                cursor.execute(
                    "DELETE FROM ping_records WHERE id = %s",
                    (ping_id,)
                )
                db_connection.commit()
            finally:
                cursor.close()
