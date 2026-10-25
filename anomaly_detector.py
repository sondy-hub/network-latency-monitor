from datetime import datetime

# ping狀態
def check_ping_status(ping):
    # 如果 ping 是 None，回傳 "failed"
    if ping is None:
        return "failed"
    
    # 如果 ping 大於 100，回傳 "high_latency"
    if ping > 100:
        return "high_latency"
    
    # 其他情況回傳 "normal"
    else:
        return "normal"


# print(check_ping_status(15))
# print(check_ping_status(120))
# print(check_ping_status(None))

# # 連續三次異常偵測
# def check_consecutive_failures(ping_results):
#     count = 0
#     for ping in ping_results:
#         if ping is None:
#             count +=1
#         else:
#             count = 0

#         if count >= 3:
#             return True

#     return False

# # 連續三次異常出現次數
# def count_anomaly_events(ping_results):
#     count = 0
#     anomaly_count = 0
#     for ping in ping_results:
#         if ping is None:
#             count += 1
#         else:
#             count = 0

#         if count == 3:
#             anomaly_count += 1

#     return anomaly_count

# 異常開始發生位置
def find_anomaly_starts(ping_results):
    starts = []
    count = 0

    for i, ping in enumerate(ping_results):
        if ping is None:
            count += 1
        else:
            count = 0

        if count == 3:
            # 將異常開始的索引加入 starts
            starts.append(i-2)

    return starts



# 連續三次異常出現次數
def count_anomaly_events(ping_results):
    return len(find_anomaly_starts(ping_results))


# 連續三次異常偵測
def check_consecutive_failures(ping_results):
    return bool(find_anomaly_starts(ping_results))

# # 異常開始時間
# def get_anomaly_times(ping_results, timestamps):
#     starts = find_anomaly_starts(ping_results)

#     anomaly_times = []

#     for i in starts:
#         anomaly_times.append(timestamps[i])

#     return anomaly_times

# 異常恢復正常位置
def find_anomaly_recoveries(ping_results):
    recoveries = []
    count = 0

    for i, ping in enumerate(ping_results):
        if ping is None:
            count += 1
        else:
            if count >= 3:
                recoveries.append(i)

            count = 0

    return recoveries


# 異常紀錄開始、恢復、持續時間
def get_anomaly_events(ping_results, timestamps):
    starts = find_anomaly_starts(ping_results)
    recoveries = find_anomaly_recoveries(ping_results)

    events = []
    
    for i, start in enumerate(starts):

        if i < len(recoveries):
            recovery = recoveries[i]
            recovery_time = timestamps[recovery]
        else:
            recovery_time = None

        start_time = timestamps[start]

        if recovery_time is not None:
            duration_seconds = (recovery_time - start_time).total_seconds()
        else:
            duration_seconds = None

        event = {
            "start_time": start_time,
            "recovery_time": recovery_time,
            "duration_seconds": duration_seconds
        }

        events.append(event)

    return events


# 建立即時異常追蹤器，異常紀錄開始、恢復、持續時間(不會重複記錄到舊資料)

class AnomalyTracker:

    def __init__(self):
        self.failure_count = 0
        self.start_time = None
        self.is_anomaly = False

    def process_ping(self, ping, timestamp):
        if ping is None:
            self.failure_count += 1

            if self.failure_count == 1:
                self.start_time = timestamp

            if self.failure_count == 3:
                self.is_anomaly = True

                return{
                    "type": "anomaly_started",
                    "start_time": self.start_time
                }
        else:
            if self.is_anomaly:
                duration_seconds = (
                    timestamp - self.start_time
                ).total_seconds()

                event = {
                    "type": "anomaly_recovered",
                    "start_time": self.start_time,
                    "recovery_time": timestamp,
                    "duration_seconds": duration_seconds
                }
            
                self.failure_count = 0
                self.start_time = None
                self.is_anomaly = False

                return event
            
            self.failure_count = 0
            self.start_time = None
            self.is_anomaly = False

        return None



class HighLatencyTracker:
    def __init__(self, threshold=70):
        self.threshold = threshold
        self.start_time = None
        self.is_anomaly = False
        self.peak_latency_ms = None

    def process_ping(self, ping, timestamp):
        if ping is None:
            return None

        if ping >= self.threshold and not self.is_anomaly: 
            self.is_anomaly = True
            self.start_time = timestamp
            self.peak_latency_ms = ping

            return{
                "type": "high_latency_started",
                "start_time": timestamp,
                "peak_latency_ms": ping
            }
        if ping >= self.threshold and self.is_anomaly:
            self.peak_latency_ms = max(self.peak_latency_ms, ping)

        if ping < self.threshold and self.is_anomaly:
            duration_seconds = (timestamp - self.start_time).total_seconds()
            event =  {
                "type": "high_latency_recovered",
                "start_time": self.start_time,
                "recovery_time": timestamp,
                "duration_seconds": duration_seconds,
                "peak_latency_ms": self.peak_latency_ms
            }

            self.is_anomaly = False
            self.start_time = None
            self.peak_latency_ms = None

            return event











