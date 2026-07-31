from app.main import app
for route in app.routes:
    if hasattr(route, 'path'):
        print(type(route).__name__, repr(getattr(route, 'path', None)), repr(getattr(route, 'name', None)))
        if hasattr(route, 'routes'):
            for child in route.routes:
                if hasattr(child, 'path'):
                    print('  child', type(child).__name__, repr(getattr(child, 'path', None)), repr(getattr(child, 'name', None)))
