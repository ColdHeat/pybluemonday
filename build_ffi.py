#!/usr/bin/python
from cffi import FFI

ffibuilder = FFI()

ffibuilder.set_source(
    "bluemonday",
    """ //passed to the real C compiler
        #include "bluemonday.h"
    """,
    extra_objects=["bluemonday.so"],
)

ffibuilder.cdef(
    """
extern long unsigned int NewPolicy();

extern long unsigned int StrictPolicy();

extern long unsigned int UGCPolicy();

extern void DestroyPolicy(long unsigned int p0);

extern void CallAttrBuilderPolicyFunction(long unsigned int p0, char* p1, char* p2, char* p3, char* p4, char* p5, char* p6);

extern void CallPolicyFunction(long unsigned int p0, char* p1);

extern void CallPolicyFunctionWithString(long unsigned int p0, char* p1, char* p2);

extern void CallPolicyFunctionWithBool(long unsigned int p0, char* p1, unsigned int p2);

extern void CallPolicyFunctionWithInt(long unsigned int policyId, char* method, char* argtype, unsigned int argument);

extern char* SanitizeWithPolicy(long unsigned int p0, char* p1);

extern void FreeCString(char* p0);
    """
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
