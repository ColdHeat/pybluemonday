package main

/*
 #include <stdlib.h>
*/
import "C"
import (
	"fmt"
	"math/rand"
	"reflect"
	"regexp"
	"unsafe"

	"github.com/microcosm-cc/bluemonday"
)

var POLICIES = map[uint64]*bluemonday.Policy{}

func GetPolicyId() uint64 {
	policyId := rand.Uint64()

	for {
		if POLICIES[policyId] == nil {
			break
		} else {
			policyId = rand.Uint64()
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
	goPolicyId := uint64(policyId)
	delete(POLICIES, goPolicyId)
}

//export CallAttrBuilderPolicyFunction
func CallAttrBuilderPolicyFunction(policyId C.ulong, policyMethod *C.char, policyArgument *C.char, valueFunction *C.char, valueFilter *C.char, selectorFunction *C.char, selectorValue *C.char) {
	goPolicyId := uint64(policyId)
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
	goPolicyId := uint64(policyId)
	goMethod := C.GoString(method)

	policy := POLICIES[goPolicyId]
	meth := reflect.ValueOf(policy).MethodByName(goMethod)
	meth.Call(nil)
}

//export CallPolicyFunctionWithString
func CallPolicyFunctionWithString(policyId C.ulong, method *C.char, argument *C.char) {
	goPolicyId := uint64(policyId)
	goMethod := C.GoString(method)
	goArgument := C.GoString(argument)

	policy := POLICIES[goPolicyId]
	args := []reflect.Value{reflect.ValueOf(goArgument)}
	meth := reflect.ValueOf(policy).MethodByName(goMethod)
	meth.Call(args)
}

//export CallPolicyFunctionWithBool
func CallPolicyFunctionWithBool(policyId C.ulong, method *C.char, argument C.uint) {
	goPolicyId := uint64(policyId)
	goMethod := C.GoString(method)
	goArgument := int(argument) != 0

	policy := POLICIES[goPolicyId]
	args := []reflect.Value{reflect.ValueOf(goArgument)}
	meth := reflect.ValueOf(policy).MethodByName(goMethod)
	meth.Call(args)
}

//export SanitizeWithPolicy
func SanitizeWithPolicy(policyId C.ulong, document *C.char) *C.char {
	goPolicyId := uint64(policyId)
	goDocument := C.GoString(document)

	policy := POLICIES[goPolicyId]
	output := policy.Sanitize(goDocument)
	return C.CString(output)
}

//export FreeCString
func FreeCString(s *C.char) {
	C.free(unsafe.Pointer(s))
}

func main() {
	var test = `<html>
		<head>
		<script type="text/javascript" src="evil-site"></script>
		<link rel="alternate" type="text/rss" src="evil-rss">
		<style>
			body {background-image: url(javascript:do_evil)};
			div {color: expression(evil)};
		</style>
		</head>
		<body onload="evil_function()">
		<!-- I am interpreted for EVIL! -->
		<a href="javascript:evil_function()">a link</a>
		<a href="#" onclick="evil_function()">another link</a>
		<p onclick="evil_function()">a paragraph</p>
		<div style="display: none">secret EVIL!</div>
		<object> of EVIL! </object>
		<iframe src="evil-site"></iframe>
		<form action="evil-site">
			Password: <input type="password" name="password">
		</form>
		<blink>annoying EVIL!</blink>
		<a href="evil-site">spam spam SPAM!</a>
		<image src="evil!">
		</body>
	</html>`
	policyId := UGCPolicy()

	CallAttrBuilderPolicyFunction(
		policyId,
		C.CString("AllowAttrs"),
		C.CString("class"),
		C.CString(""),
		C.CString(""),
		C.CString("Globally"),
		C.CString(""),
	)

	CallPolicyFunction(policyId, C.CString("AllowDataURIImages"))

	CallPolicyFunctionWithString(policyId, C.CString("AllowElements"), C.CString("style"))

	CallPolicyFunctionWithBool(policyId, C.CString("RequireNoReferrerOnLinks"), 1)
	CallPolicyFunctionWithBool(policyId, C.CString("AddTargetBlankToFullyQualifiedLinks"), 1)

	output := C.GoString(SanitizeWithPolicy(policyId, C.CString(test)))
	fmt.Println(output)
}
