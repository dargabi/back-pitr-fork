import functools

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # Si no está logueado, redirigir a login
        # return no autorizado 

        return view(**kwargs)

    return wrapped_view