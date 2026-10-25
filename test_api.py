from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
import pytest
# Mock()：自己建立一個假的物件，但不會自動取代任何函式。
# patch()：暫時替換指定位置的物件，預設會自動建立 MagicMock，離開作用範圍後恢復原狀。


client = TestClient(app)

def test_get_high_latency_events():
    fake_data = [
        {
            "id": 1,
            "peak_latency_ms": 250,
            "threshold_ms": 70
        }
    ]

    with patch("main.get_connection") as mock_connection, \
         patch("main.get_high_latency_events") as mock_query:

        mock_query.return_value = fake_data

        response = client.get("/api/high-latency?limit=10")

        assert response.status_code == 200
        assert response.json() == fake_data

        # 檢查被模擬的函式是否剛好呼叫一次，而且傳入的參數符合預期。
        mock_query.assert_called_once_with(
            mock_connection.return_value,
            10
        )

        mock_connection.return_value.close.assert_called_once()


def test_high_latency_invalid_limit():
    response = client.get("/api/high-latency?limit=0")

    assert response.status_code == 422




def test_high_latency_database_error():
    with patch("main.get_connection") as mock_connection, \
         patch("main.get_high_latency_events") as mock_query:

        mock_query.side_effect = Exception("資料庫查詢失敗")

        with pytest.raises(Exception, match="資料庫查詢失敗"):
            client.get("/api/high-latency")

        # 請你在這裡補上檢查資料庫連線是否關閉的 assert
        mock_connection.return_value.close.assert_called_once()