let {PythonShell} = require('python-shell')
var path = require("path")



function build_product() {
  var e = document.getElementById("productname");
  var product = e.options[e.selectedIndex].value;
  var go = document.getElementById("btn-go");
  var version = document.getElementById("input_version").value
  e.disabled = "true";
  go.disabled = "true";

  //console.log(product)

  
  var options = {
    scriptPath : path.join(__dirname, '/../engine/'),
    args : [product, window.user, window.password, version],
    //need below for production... could probably use __dirname like above
    pythonPath : path.join(__dirname, '/../dist/warlockupdate/warlockupdate.exe')
  }
  
  let pyshell = new PythonShell('warlockupdate.py', options);
  pyshell.on('message', function(message) {
  // swal(message);
    console.log(message);
    post_results(1);
  })
  .on('uncaughtException', (err) => {
    console.error('there was an uncaught error', err);
    post_results(0);
    
  })


}
//i need to try catch something above... fatal error in python does not seem to get caught...hmmmmmm

function post_results(result){
  var e = document.getElementById("productname");
  var go = document.getElementById("btn-go");
  e.disabled = false;
  go.disabled = false;
  results_pane = document.getElementById("results-pane");
  results_div = document.getElementById("results-div");
  console.log(result);
  results_div.classList.remove("hide-me");
  if (document.contains(document.getElementById("results"))) {
    document.getElementById("results").remove();
  }   
  if (result == 1) {
 //   results_pane.innerHTML = "Complete! Maybe not successfully, but I sure am done!";
    var str = '<div class="alert alert-success alert-dismissible fade show" id="results" role="alert"><strong>Complete!</strong> Maybe not successful really, but I sure am done.<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
      //results_pane.insertAdjacentHTML('beforeend', str )
  }
  else {
    var str = '<div class="alert alert-dismissible alert-danger fade show" id="results" role="alert">This failed. Horribly.<p><strong>grats</strong></p><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
 //   results_pane.innerHTML = "Complete! This failed. Horribly.";
  }
  results_pane.insertAdjacentHTML('beforeend', str )
}

function fade_signin() {
  //window allows me to declare global variable. since i delete these fields but i need them in build product.
  console.log("Preparing fadeout");
  window.user = document.getElementById("input_user").value
  window.password = document.getElementById("input_password").value
  element = document.getElementById("login");
  element.classList.add("fade-out");
  //setTimeout(remove_signin, 3000)
  console.log("Fadeout initiated")
  swal("Successful login!").then(()=> {

  this.remove_signin(); // this should execute now

})
  
  //element.parentNode.removeChild(element);
  //product = document.getElementById("product_selection");
  //product.classList.remove(".hide-me");
  //product.style.display="flex";
  //console.log(product)
}

function remove_signin() {
  console.log("Removing signin")
  element = document.getElementById("login");
  element.parentNode.removeChild(element);
  //product = document.getElementById("product_selection");
 //product.classList.add("fade-in");
  console.log("Showing vault details")
  product = document.getElementById("vault-div");
  product.classList.remove("hide-me");
  document.getElementById("page-label").innerHTML = "Vault Details";
  product.style.display="flex";

}
