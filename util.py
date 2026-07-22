class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    def destroy(cls):
        cls._instances.pop(cls, None)

class Multiton(type):
    _instances = {}

    def __call__(cls, key, *args, **kwargs):
        instance_key = (cls, key)

        if instance_key not in cls._instances:
            cls._instances[instance_key] = super().__call__(key, *args, **kwargs)

        return cls._instances[instance_key]

    def destroy(cls, key=None):
        if key is None:
            # 해당 클래스의 모든 인스턴스 삭제
            for k in list(cls._instances):
                if k[0] == cls:
                    del cls._instances[k]
        else:
            cls._instances.pop((cls, key), None)

from display import Screen as Window

class Timer(metaclass=Multiton):
    window : Window

    @classmethod
    def init(cls, window):
        cls.window : Window = window

    @classmethod
    def update_all(cls):
        for timer in Multiton._instances.values():
            if timer.__class__ is cls:
                timer.update()

    def __init__(self, name):
        self.name = name
        self.time = 0.0
        self.running = False
        self.triggered = set()

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def reset(self):
        self.time = 0.0
        self.triggered.clear()

    def update(self):
        if self.running:
            self.time += self.window.dt

    from collections.abc import Callable

    def trigger(self, trigger_time : int | float, meta_func : Callable | None =None) -> bool:
        """_summary_

        Args:
            trigger_time (int | float): Activated at the "trigger_time" time
            meta_func (Callable | None, optional): Execute a preprocessing function, similar to a metaclass hook, before activating the trigger, then return True. Defaults to None.

        Returns:
            bool: _description_
        """
        if trigger_time not in self.triggered and self.time >= trigger_time:
            self.triggered.add(trigger_time)

            if callable(meta_func):
                meta_func()

            return True

        return False

class SignalDB:
    listeners = {}
    history = []
    sequence = 0

    @classmethod
    def emit(cls, signal):
        signal.id = cls.sequence
        cls.sequence += 1
        cls.history.append(signal)

        for func in cls.listeners.get(signal.name, []):
            func(signal)

    def receive(self):

class Signal:
    def __init__(self, name, sender, data):
        self.id = 0
        self.name = name
        self.sender = sender
        self.data = data
        self.time = Timer("game_time").time

SignalDB.emit(Signal("test", "self", "data"))