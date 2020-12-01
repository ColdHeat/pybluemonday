from pybluemonday.bluemonday import ffi, lib
from typing import List


class AttrPolicyBuilder:
    def __init__(self, policy_id, policy_method, attrs):
        self.policy_id = policy_id
        self.policy_method = policy_method
        self.attrs = attrs
        self.attr_value_function = None
        self.attr_value_filter = None
        self.selector_function = None
        self.selector_value = None

    # Format
        # Policy Method (AllowAttrs, AllowNoAttrs)
        # Attributes (class, style)
        # Value Function (Matching)
        # Value Filter (regex value)
        # Selector Function (OnElements, OnElementsMatching, Globally)
        # Selector Value (string, regex value, or nil)

    def Matching(self, regex):
        pass

    def OnElements(self, *elements):
        for attr in self.attrs:
            for elem in elements:
                lib.CallAttrBuilderPolicyFunction(
                    self.policy_id,
                    self.policy_method.encode(),
                    attr.encode(),
                    b"OnElements",
                    elem.encode()
                )

    def OnElementsMatching(self, regex):
        pass

    def Globally(self):
        for attr in self.attrs:
            # Pass an empty string. We check for empty string in the last argument and set it to nil
            lib.CallAttrBuilderPolicyFunction(
                self.policy_id,
                self.policy_method.encode(),
                attr.encode(),
                b"Globally",
                b""
            )


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

    def AllowAttrs(self, *attrs):
        return AttrPolicyBuilder(
            policy_id=self._id, policy_method="AllowAttrs", attrs=attrs
        )

    def AllowNoAttrs(self, *attrs):
        return AttrPolicyBuilder(
            policy_id=self._id, policy_method="AllowNoAttrs", attrs=attrs
        )

    # # AllowAttrsGlobally
    # def AllowAttrsGlobally(self, attrs: List[str]):
    #     for attr in attrs:
    #         lib.AllowAttrGlobally(self._id, attr.encode())

    # # AllowAttrsOnElements
    # def AllowAttrsOnElements(self, attrs: List[str], elements: List[str]):
    #     for attr in attrs:
    #         for element in elements:
    #             lib.AllowAttrOnElement(self._id, attr.encode(), element.encode())

    # # AllowAttrsOnElementsMatching
    # def AllowAttrsOnElementsMatching(self, attrs: List[str], regex: str):
    #     for attr in attrs:
    #         lib.AllowAttrsOnElementsMatching(self._id, attr.encode(), regex.encode())

    # # AllowMatchingAttrsGlobally
    # def AllowMatchingAttrsGlobally(self, attrs, attrs_regex):
    #     for attr in attrs:
    #         for regex in attrs_regex:
    #             lib.AllowMatchingAttrsGlobally(self._id, attr.encode(), regex.encode())

    # # AllowMatchingAttrsOnElements
    # def AllowMatchingAttrsOnElements(self, attrs, attrs_regex, elements):
    #     for attr in attrs:
    #         for regex in attrs_regex:
    #             for elem in elements:
    #                 lib.AllowMatchingAttrsOnElements(
    #                     self._id, attr.encode(), regex.encode()
    #                 )

    # # AllowMatchingAttrsOnElementsMatching
    # def AllowMatchingAttrsOnElementsMatching(self, attrs_regex, elements_regex):
    #     for attr in attrs:
    #         for attr_regex in attrs_regex:
    #             for elem_regex in elements_regex:
    #                 lib.AllowMatchingAttrsOnElementsMatching(
    #                     self._id,
    #                     attr.encode(),
    #                     attr_regex.encode(),
    #                     elem_regex.encode(),
    #                 )

    def sanitize(self, document):
        if isinstance(document, str):
            document = document.encode()

        output = lib.SanitizeWithPolicy(self._id, document)
        return ffi.string(output).decode()

    def __del__(self):
        lib.DestroyPolicy(self._id)
