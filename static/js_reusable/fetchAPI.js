function fetchAPI(url) {
    // The httpReq Object is now local to function "ajaxCall" (not global)
    var httpReq;
    if (window.XMLHttpRequest) {
        httpReq = new XMLHttpRequest(); //For Firefox, Safari, Opera
    } else if (window.ActiveXObject) {
        httpReq = new ActiveXObject("Microsoft.XMLHTTP"); //For IE 5+
    } else {
        alert('ajax not supported');
    }

    console.log("ready to get content " + url);
    httpReq.open("GET", url); // specify which page you want to get

    // Ajax calls are asyncrhonous (non-blocking). Specify the code that you 
    // want to run when the response (to the http request) is available. 
    httpReq.onreadystatechange = callBack;
    httpReq.send(null); // initiate ajax call
    function callBack() {
        
        // readyState == 4 means that the http request is complete
        if (httpReq.readyState === 4) {
            if (httpReq.status === 200) {
                var jsObj = JSON.parse(httpReq.responseText);
                console.log("ajax_alt success: will send obj (see next line)");
                console.log(jsObj);
                return jsObj;
            } else {
                var eMsg = "Error (" + httpReq.status + " " + httpReq.statusText +
                        ") while attempting to read '" + url + "'";
                console.log("ajax_alt failure error is " + eMsg);
                return null;
            }
        }
    } // end of callBack
}