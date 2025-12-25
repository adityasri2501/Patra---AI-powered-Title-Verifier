def init_trace():
    return []

def add_trace(trace, step, detail):
    trace.append({
        "step": step,
        "detail": detail
    })
