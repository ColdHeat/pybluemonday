from pybluemonday.bluemonday import ffi, lib


class Sanitizer:
    def __init__(self):
        self._id = lib.NewUGCPolicy()

    def __getattr__(self, attr):
        def method(*args):
            method_name = attr.encode()
            if args:
                if isinstance(args[0], str):
                    string_arg = args[0].encode()
                    lib.CallPolicyFunctionWithString(self._id, method_name, string_arg)
                elif isinstance(args[0], bool):
                    bool_arg = int(args[0])
                    lib.CallPolicyFunctionWithBool(self._id, method_name, bool_arg)
            else:
                lib.CallPolicyFunction(self._id, method_name)

        return method

    def sanitize(self, document):
        if isinstance(document, str):
            document = document.encode()

        output = lib.SanitizeWithPolicy(self._id, document)
        return ffi.string(output).decode()

    def __del__(self):
        lib.DestroyPolicy(self._id)
