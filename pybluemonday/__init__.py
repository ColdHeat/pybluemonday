from typing import List
from unicodedata import normalize

from pybluemonday.bluemonday import ffi, lib

__version__ = "0.0.4"


class AttrPolicyBuilder:
    def __init__(self, policy_id: int, policy_method: str, attrs: List[str]):
        self.policy_id = policy_id
        self.policy_method = policy_method
        self.attrs = attrs
        self.attr_value_function = ""
        self.attr_value_filter = ""
        self.selector_function = ""
        self.selector_value = ""

    # Format
    # Policy Method (AllowAttrs, AllowNoAttrs)
    # Attributes (class, style)
    # Value Function (Matching)
    # Value Filter (regex value)
    # Selector Function (OnElements, OnElementsMatching, Globally)
    # Selector Value (string, regex value, or nil)

    def Matching(self, regex):
        self.attr_value_function = "Matching"
        self.attr_value_filter = regex

    def OnElements(self, *elements):
        for attr in self.attrs:
            for elem in elements:
                lib.CallAttrBuilderPolicyFunction(
                    self.policy_id,
                    self.policy_method.encode(),
                    attr.encode(),
                    self.attr_value_function.encode(),
                    self.attr_value_filter.encode(),
                    b"OnElements",
                    elem.encode(),
                )

    def OnElementsMatching(self, regex):
        for attr in self.attrs:
            lib.CallAttrBuilderPolicyFunction(
                self.policy_id,
                self.policy_method.encode(),
                attr.encode(),
                self.attr_value_function.encode(),
                self.attr_value_filter.encode(),
                b"OnElementsMatching",
                regex.encode(),
            )

    def Globally(self):
        for attr in self.attrs:
            lib.CallAttrBuilderPolicyFunction(
                self.policy_id,
                self.policy_method.encode(),
                attr.encode(),
                self.attr_value_function.encode(),
                self.attr_value_filter.encode(),
                b"Globally",
                b"",
            )


class Policy:
    def __init__(self):
        self._id = lib.NewPolicy()

    def __getattr__(self, attr: str):
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

    def AllowAttrs(self, *attrs: str):
        return AttrPolicyBuilder(
            policy_id=self._id, policy_method="AllowAttrs", attrs=attrs
        )

    def AllowNoAttrs(self, *attrs: str):
        return AttrPolicyBuilder(
            policy_id=self._id, policy_method="AllowNoAttrs", attrs=attrs
        )

    def sanitize(self, document):
        if isinstance(document, str):
            document = document.encode()

        output = lib.SanitizeWithPolicy(self._id, document)
        b = ffi.string(output).decode()
        lib.FreeCString(output)
        return normalize("NFKD", b)

    def __del__(self):
        lib.DestroyPolicy(self._id)


class NewPolicy(Policy):
    def __init__(self):
        self._id = lib.NewPolicy()


class StrictPolicy(Policy):
    def __init__(self):
        self._id = lib.StrictPolicy()


class UGCPolicy(Policy):
    def __init__(self):
        self._id = lib.UGCPolicy()
