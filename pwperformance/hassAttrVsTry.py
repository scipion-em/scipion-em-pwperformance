from pwperformance.main import Timer

with Timer(msg="hasAttr") as t:
    for i in range(1**6):
        if hasattr(t, "missing"):
            pass


with Timer(msg="tryExcept") as t:
    for i in range(1**6):
        try:
            pass
        except Exception as e:
            pass