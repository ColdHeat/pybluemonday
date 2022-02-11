package main

/*
 #include <stdlib.h>
*/
import "C"
import (
	"math/rand"
	"reflect"
	"regexp"
	"unsafe"

	"github.com/microcosm-cc/bluemonday"
)

var POLICIES = map[uint32]*bluemonday.Policy{}

func GetPolicyId() uint32 {
	policyId := rand.Uint32()

	for {
		if POLICIES[policyId] == nil {
			break
		} else {
			policyId = rand.Uint32()
		}
	}
	return policyId
}

//export NewPolicy
func NewPolicy() C.ulong {
	policyId := GetPolicyId()
	policy := bluemonday.NewPolicy()
	POLICIES[policyId] = policy
	return C.ulong(policyId)
}

//export StrictPolicy
func StrictPolicy() C.ulong {
	policyId := GetPolicyId()
	policy := bluemonday.StrictPolicy()
	POLICIES[policyId] = policy
	return C.ulong(policyId)
}

//export UGCPolicy
func UGCPolicy() C.ulong {
	policyId := GetPolicyId()
	policy := bluemonday.UGCPolicy()
	POLICIES[policyId] = policy
	return C.ulong(policyId)
}

//export DestroyPolicy
func DestroyPolicy(policyId C.ulong) {
	goPolicyId := uint32(policyId)
	delete(POLICIES, goPolicyId)
}

//export CallAttrBuilderPolicyFunction
func CallAttrBuilderPolicyFunction(policyId C.ulong, policyMethod *C.char, policyArgument *C.char, valueFunction *C.char, valueFilter *C.char, selectorFunction *C.char, selectorValue *C.char) {
	goPolicyId := uint32(policyId)
	goPolicyMethod := C.GoString(policyMethod)
	goPolicyArgument := C.GoString(policyArgument)
	goValueFunction := C.GoString(valueFunction)
	goValueFilter := C.GoString(valueFilter)
	goSelectorFunction := C.GoString(selectorFunction)
	goSelectorValue := C.GoString(selectorValue)

	policy := POLICIES[goPolicyId]
	switch goPolicyMethod {
	case "AllowAttrs":
		AttrPolicyBuilder := policy.AllowAttrs(goPolicyArgument)
		if len(goValueFunction) > 0 {
			switch goPolicyMethod {
			case "Matching":
				valueRegex := regexp.MustCompile(goValueFilter)
				AttrPolicyBuilder.Matching(valueRegex)
			default:
				panic("Unknown value function")
			}
		}

		switch goSelectorFunction {
		case "OnElements":
			AttrPolicyBuilder.OnElements(goSelectorValue)
		case "OnElementsMatching":
			selectorRegex := regexp.MustCompile(goSelectorValue)
			AttrPolicyBuilder.OnElementsMatching(selectorRegex)
		case "Globally":
			AttrPolicyBuilder.Globally()
		default:
			panic("Unknown selector function")
		}

	case "AllowNoAttrs":
		AttrPolicyBuilder := policy.AllowNoAttrs()
		if len(goValueFunction) > 0 {
			switch goPolicyMethod {
			case "Matching":
				valueRegex := regexp.MustCompile(goValueFilter)
				AttrPolicyBuilder.Matching(valueRegex)
			default:
				panic("Unknown value function")
			}
		}

		switch goSelectorFunction {
		case "OnElements":
			AttrPolicyBuilder.OnElements(goSelectorValue)
		case "OnElementsMatching":
			selectorRegex := regexp.MustCompile(goSelectorValue)
			AttrPolicyBuilder.OnElementsMatching(selectorRegex)
		case "Globally":
			AttrPolicyBuilder.Globally()
		default:
			panic("Unknown selector function")
		}
	default:
		panic("Unknown policy method")
	}
}

//export CallPolicyFunction
func CallPolicyFunction(policyId C.ulong, method *C.char) {
	goPolicyId := uint32(policyId)
	goMethod := C.GoString(method)

	policy := POLICIES[goPolicyId]
	meth := reflect.ValueOf(policy).MethodByName(goMethod)
	meth.Call(nil)
}

//export CallPolicyFunctionWithString
func CallPolicyFunctionWithString(policyId C.ulong, method *C.char, argument *C.char) {
	goPolicyId := uint32(policyId)
	goMethod := C.GoString(method)
	goArgument := C.GoString(argument)

	policy := POLICIES[goPolicyId]
	args := []reflect.Value{reflect.ValueOf(goArgument)}
	meth := reflect.ValueOf(policy).MethodByName(goMethod)
	meth.Call(args)
}

//export CallPolicyFunctionWithBool
func CallPolicyFunctionWithBool(policyId C.ulong, method *C.char, argument C.uint) {
	goPolicyId := uint32(policyId)
	goMethod := C.GoString(method)
	goArgument := int(argument) != 0

	policy := POLICIES[goPolicyId]
	args := []reflect.Value{reflect.ValueOf(goArgument)}
	meth := reflect.ValueOf(policy).MethodByName(goMethod)
	meth.Call(args)
}

//export CallPolicyFunctionWithInt
func CallPolicyFunctionWithInt(policyId C.ulong, method *C.char, argtype *C.char, argument C.uint) {
	goPolicyId := uint32(policyId)
	goMethod := C.GoString(method)
	goArgType := C.GoString(argtype)
	goArgument := int(argument)
	policy := POLICIES[goPolicyId]

	switch goArgType {
	case "SandboxValue":
		sv := bluemonday.SandboxValue(goArgument)
		args := []reflect.Value{reflect.ValueOf(sv)}
		meth := reflect.ValueOf(policy).MethodByName(goMethod)
		meth.Call(args)
	default:
		panic("Unknown argument type function")
	}
}

//export SanitizeWithPolicy
func SanitizeWithPolicy(policyId C.ulong, document *C.char) *C.char {
	goPolicyId := uint32(policyId)
	goDocument := C.GoString(document)

	policy := POLICIES[goPolicyId]
	output := policy.Sanitize(goDocument)
	return C.CString(output)
}

//export FreeCString
func FreeCString(s *C.char) {
	C.free(unsafe.Pointer(s))
}

func main() {}
