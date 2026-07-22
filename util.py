class Timer:
    """필요할 때 독립적으로 사용할 수 있는 작은 타이머."""
    def __init__(self): self.time = 0.0; self.running = False
    def start(self, reset=False):
        if reset: self.time = 0.0
        self.running = True
    def stop(self): self.running = False
    def reset(self): self.time = 0.0
    def update(self, dt):
        if self.running: self.time += dt
    def reached(self, seconds): return self.time >= seconds


class SignalDB:
    def __init__(self): self.listeners = {}; self.history = []
    def connect(self, name, callback): self.listeners.setdefault(name, []).append(callback)
    def emit(self, name, data=None):
        self.history.append((name, data))
        for callback in self.listeners.get(name, []): callback(data)
