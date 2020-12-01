package main

import (
	"C"
	"fmt"
	"github.com/microcosm-cc/bluemonday"
	"math/rand"
	"reflect"
	// "regexp"
)

var POLICIES = map[uint64]*bluemonday.Policy{}

//export NewPolicy
func NewPolicy() C.ulong {
	policyId := rand.Uint64()
	policy := bluemonday.NewPolicy()
	POLICIES[policyId] = policy
	return C.ulong(policyId)
}

//export StrictPolicy
func StrictPolicy() C.ulong {
	policyId := rand.Uint64()
	policy := bluemonday.StrictPolicy()
	POLICIES[policyId] = policy
	return C.ulong(policyId)
}

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

// //export AllowAttrGlobally
// func AllowAttrGlobally(policyId C.ulong, attr *C.char) {
// 	goPolicyId := uint64(policyId)
// 	goAttr := C.GoString(attr)

// 	policy := POLICIES[goPolicyId]
// 	policy.AllowAttrs(goAttr).Globally()
// }

// //export AllowAttrOnElement
// func AllowAttrOnElement(policyId C.ulong, attr *C.char, element *C.char) {
// 	goPolicyId := uint64(policyId)
// 	goAttr := C.GoString(attr)
// 	goElement := C.GoString(element)

// 	policy := POLICIES[goPolicyId]
// 	policy.AllowAttrs(goAttr).OnElements(goElement)
// }

// //export AllowAttrsOnElementsMatching
// func AllowAttrsOnElementsMatching(policyId C.ulong, attr *C.char, regex *C.char) {
// 	goPolicyId := uint64(policyId)
// 	goAttr := C.GoString(attr)
// 	goRegex := C.GoString(regex)

// 	elementRegex := regexp.MustCompile(goRegex)

// 	policy := POLICIES[goPolicyId]
// 	policy.AllowAttrs(goAttr).OnElementsMatching(elementRegex)
// }

// //export AllowMatchingAttrsGlobally
// func AllowMatchingAttrsGlobally(policyId C.ulong, attr *C.char, regex *C.char) {
// 	goPolicyId := uint64(policyId)
// 	goAttr := C.GoString(attr)
// 	goRegex := C.GoString(regex)

// 	attrValueRegex := regexp.MustCompile(goRegex)

// 	policy := POLICIES[goPolicyId]
// 	policy.AllowAttrs(goAttr).Matching(attrValueRegex).Globally()
// }

// //export AllowMatchingAttrsOnElements
// func AllowMatchingAttrsOnElements(policyId C.ulong, attr *C.char, regex *C.char, element *C.char) {
// 	goPolicyId := uint64(policyId)
// 	goAttr := C.GoString(attr)
// 	goRegex := C.GoString(regex)
// 	goElement := C.GoString(element)

// 	attrValueRegex := regexp.MustCompile(goRegex)

// 	policy := POLICIES[goPolicyId]
// 	policy.AllowAttrs(goAttr).Matching(attrValueRegex).OnElements(goElement)
// }

// //AllowMatchingAttrsOnElementsMatching
// func AllowMatchingAttrsOnElementsMatching(policyId C.ulong, attr *C.char, attrRegex *C.char, elementRegex *C.char) {
// 	goPolicyId := uint64(policyId)
// 	goAttr := C.GoString(attr)
// 	goAttrValueRegex := regexp.MustCompile(C.GoString(attrRegex))
// 	goElementRegex := regexp.MustCompile(C.GoString(elementRegex))

// 	policy := POLICIES[goPolicyId]
// 	policy.AllowAttrs(goAttr).Matching(goAttrValueRegex).OnElementsMatching(goElementRegex)
// }

//export CallAttrBuilderPolicyFunction
func CallAttrBuilderPolicyFunction(policyId C.ulong, policyMethod *C.char, policyArgument *C.char, builderMethod *C.char, builderArgument *C.char) {
	// policy.AllowAttrs("method", "action").OnElements("form")
	goPolicyId := uint64(policyId)
	goPolicyMethod := C.GoString(policyMethod)
	goPolicyArgument := C.GoString(policyArgument)
	goBuilderMethod := C.GoString(builderMethod)
	goBuilderArgument := C.GoString(builderArgument)

	policy := POLICIES[goPolicyId]
	var AttrPolicyBuilder interface{}
	switch goPolicyMethod {
	case "AllowAttrs":
		AttrPolicyBuilder = policy.AllowAttrs(goPolicyArgument)
	case "AllowNoAttrs":
		AttrPolicyBuilder = policy.AllowNoAttrs()
	default:
		panic("Unknown policy method")
	}

	meth := reflect.ValueOf(AttrPolicyBuilder).MethodByName(goBuilderMethod)
	if (goBuilderMethod == "Globally") {
		meth.Call(nil)
		return
	} else {
		args := []reflect.Value{reflect.ValueOf(goBuilderArgument)}
		meth.Call(args)
		return
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

func main() {
	// 	var test = `<html>
	// 	<head>
	// 	<script type="text/javascript" src="evil-site"></script>
	// 	<link rel="alternate" type="text/rss" src="evil-rss">
	// 	<style>
	// 		body {background-image: url(javascript:do_evil)};
	// 		div {color: expression(evil)};
	// 	</style>
	// 	</head>
	// 	<body onload="evil_function()">
	// 	<!-- I am interpreted for EVIL! -->
	// 	<a href="javascript:evil_function()">a link</a>
	// 	<a href="#" onclick="evil_function()">another link</a>
	// 	<p onclick="evil_function()">a paragraph</p>
	// 	<div style="display: none">secret EVIL!</div>
	// 	<object> of EVIL! </object>
	// 	<iframe src="evil-site"></iframe>
	// 	<form action="evil-site">
	// 		Password: <input type="password" name="password">
	// 	</form>
	// 	<blink>annoying EVIL!</blink>
	// 	<a href="evil-site">spam spam SPAM!</a>
	// 	<image src="evil!">
	// 	</body>
	// </html>`

	test := `
<div class="row">
    <div class="col-md-6 offset-md-3" yeet="asdf">
        <img yeet="asdf" class="w-100 mx-auto d-block" style="max-width: 500px;padding: 50px;padding-top: 14vh;" src="themes/core/static/img/logo.png" />
        <h3 class="text-center">
            <p>A cool CTF platform from <a href="https://ctfd.io">ctfd.io</a></p>
            <p>Follow us on social media:</p>
            <a href="https://twitter.com/ctfdio"><i class="fab fa-twitter fa-2x" aria-hidden="true"></i></a>&nbsp;
            <a href="https://facebook.com/ctfdio"><i class="fab fa-facebook fa-2x" aria-hidden="true"></i></a>&nbsp;
            <a href="https://github.com/ctfd"><i class="fab fa-github fa-2x" aria-hidden="true"></i></a>
        </h3>
        <table test="asdf">
            <thead test="fdsa">
                <select>
                    <option>asdf</option>
                </select>
            </thead>
        </table>
        <br>
        <h4 class="text-center">
            <a href="admin">Click here</a> to login and setup your CTF
        </h4>
    </div>
</div>
`
	policyId := NewUGCPolicy()

	CallAttrBuilderPolicyFunction(
		policyId,
		C.CString("AllowAttrs"),
		C.CString("class"),
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
