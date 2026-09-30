"""示例服务的 HTTP 入口：暴露业务接口 + Prometheus /metrics，供第 2 周可观测性练习。"""
from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from app.calc import add, divide

app = Flask(__name__)

ADD_COUNT = Counter("calc_add_total", "add 接口调用次数")
DIVIDE_COUNT = Counter("calc_divide_total", "divide 接口调用次数")
REQ_LATENCY = Histogram("calc_request_latency_seconds", "接口请求耗时", ["path"])


@app.get("/add")
def add_ep():
    ADD_COUNT.inc()
    with REQ_LATENCY.labels(path="/add").time():
        a = float(request.args.get("a", 0))
        b = float(request.args.get("b", 0))
        return jsonify(result=add(a, b))


@app.get("/divide")
def divide_ep():
    DIVIDE_COUNT.inc()
    with REQ_LATENCY.labels(path="/divide").time():
        a = float(request.args.get("a", 0))
        b = float(request.args.get("b", 1))
        try:
            return jsonify(result=divide(a, b))
        except ValueError as e:
            return jsonify(error=str(e)), 400


@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


@app.get("/healthz")
def healthz():
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
