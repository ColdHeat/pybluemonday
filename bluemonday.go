package main

import (
	"C"
	"fmt"
	"github.com/microcosm-cc/bluemonday"
	"math/rand"
	"reflect"
)

var POLICIES = map[uint64]*bluemonday.Policy{}

//export NewUGCPolicy
func NewUGCPolicy() C.ulong {
	policyId := rand.Uint64()
	policy := bluemonday.UGCPolicy()
	POLICIES[policyId] = policy
	return C.ulong(policyId)
}

//export DestroyPolicy
func DestroyPolicy(policyId C.ulong) {
	goPolicyId := uint64(policyId)
	delete(POLICIES, goPolicyId)
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

	policyId := NewUGCPolicy()

	CallPolicyFunction(policyId, C.CString("AllowDataURIImages"))

	CallPolicyFunctionWithString(policyId, C.CString("AllowElements"), C.CString("style"))

	CallPolicyFunctionWithBool(policyId, C.CString("RequireNoReferrerOnLinks"), 1)

	output := C.GoString(SanitizeWithPolicy(policyId, C.CString(test)))
	fmt.Println(output)
}
