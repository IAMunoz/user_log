$(document).ready(function(){
    $("#email").blur(checkEmail)
})

function checkEmail(){
    var data = $("#formRegister").serialize()
    
    $.ajax({
        method: "POST",
        url: "/checkEmail",
        data: data,
        dataType: "JSON",
 
    })   
    .done (function (response) {
        var size = Object.keys(response['errors']).length;
        if (size > 0) {
            console.log(response['errors'])
            alert("Revisa que tu email esta correcto")
        }
        else {
            console.log('Correo Valido')
            
        }
        
    })
}
