from functools import wraps


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the correct number of arguments."
        except KeyError:
            return "Key not found."
        except IndexError:
            return "Not found. Index is out of range."
        except Exception as e:
            return f"Unexpected error: {str(e)}"

    return inner
