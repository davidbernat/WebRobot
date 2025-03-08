from multiprocessing import pool


# should simplify the cloudnode code to match this.
class ParallelizePool:
    """a simple multi-use class for running a function in n_thread parallel protected function calls """
    def __init__(self, n_threads=10):
        self.pool = pool.ThreadPool(processes=n_threads)

    def starmap(self, function, arguments, on_error_value=None, protected_throws=True):
        """execute function for each of arguments [args1, args2...]. returns array of return values or on_error_value"""
        if len(arguments) == 0: return []
        if protected_throws:
            try: results = self.pool.starmap(function, arguments)
            except: results = on_error_value
        else: results = self.pool.starmap(function, arguments)
        return results
