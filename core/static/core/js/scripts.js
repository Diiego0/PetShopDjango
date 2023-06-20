
function hideDescription(card) {
  var desc = card.querySelector('.oferta');
  desc.style.display = 'none';
}

function showDescription(card) {
  var desc = card.querySelector('.oferta');
  desc.style.display = 'block';
}

function hideDescription2(card) {
  var desc = card.querySelector('.butoncito');
  desc.style.display = 'none';
}

function showDescription2(card) {
  var desc = card.querySelector('.butoncito');
  desc.style.display = 'block';
}


$(document).ready(function(){
  // Agregar método de validación para RUT chileno
  $.validator.addMethod("rutChileno", function(value, element) {
    // Eliminar puntos y guión del RUT
    value = value.replace(/[.-]/g, "");

    // Validar que el RUT tenga 8 o 9 dígitos
    if (value.length < 8 || value.length > 9) {
      return false;
    }

    // Validar que el último dígito sea un número o una 'K'
    var validChars = "0123456789K";
    var lastChar = value.charAt(value.length - 1).toUpperCase();
    if (validChars.indexOf(lastChar) == -1) {
      return false;
    }

    // Calcular el dígito verificador
    var rut = parseInt(value.slice(0, -1), 10);
    var factor = 2;
    var sum = 0;
    var digit;
    while (rut > 0) {
      digit = rut % 10;
      sum += digit * factor;
      rut = Math.floor(rut / 10);
      factor = factor === 7 ? 2 : factor + 1;
    }
    var dv = 11 - (sum % 11);
    dv = dv === 11 ? "0" : dv === 10 ? "K" : dv.toString();

    // Validar que el dígito verificador sea correcto
    return dv === lastChar;
  }, "Por favor ingrese un RUT válido."); 





$(document).ready(function() {
    $("#formreg").validate({
        rules: {
          inputnombres4: {
            required: true,
          },
          inputapellidos4: {
            required: true,
          },
          inputEmail4: {
            required: true,
            email: true,
          },
          inputrut4: {
            required: true,
            rutChileno: true,
          },
          floatingTextarea2: {
            required: true,
          },
          inputPassword1: {
            required: true,
            minlength: 6,
          },
          inputPassword4: {
            required: true,
            equalTo: "#inputPassword1",
          },
          inputImage: {
            required: true,
          },
        }, // Fin de reglas
        messages: {
          inputnombres4: {
            required: "Por favor ingresa tus nombres",
          },
          inputapellidos4: {
            required: "Por favor ingresa tus apellidos",
          },
          inputEmail4: {
            required: "Por favor ingresa tu email",
            email: "Por favor ingresa un email válido",
          },
          inputrut4: {
            required: "Por favor ingresa tu RUT",
          },
          floatingTextarea2: {
            required: "Por favor ingresa tu dirección",
          },
          inputPassword1: {
            required: "Por favor ingresa una contraseña",
            minlength: "La contraseña debe tener al menos 6 caracteres",
          },
          inputPassword4: {
            required: "Por favor confirma tu contraseña",
            equalTo: "Las contraseñas no coinciden",
          },
          inputImage: {
            required: "Por favor ingresa una imagen",
          },
        },
      });
  });

$(document).ready(function () {

  $.get('https://fakestoreapi.com/products/category/men\'s%20clothing', function (data) {

    $.each(data, function (i, item) {

      var card = '';
      card += '<div class="col-lg-3 col-md-4 col-sm-6 mb-4">';
      card += '  <div class="card h-100">';
      card += '    <img src="' + item.image + '" class="card-img-top" alt="' + item.title + '">';
      card += '    <div class="card-body">';
      card += '      <h5 class="card-title truncate">' + item.title + '</h5>';
      card += '      <p class="card-text">';
      card += '        <span class="stock">' + item.category + '</span>';
      card += '      </p>';
      card += '    </div>';
      card += '  </div>';
      card += '</div>';

      $('#contenedor-productos').append(card);

    });

  });

  $.get('https://fakestoreapi.com/products/category/women\'s%20clothing', function (data) {

    $.each(data, function (i, item) {

      var card = '';
      card += '<div class="col-lg-3 col-md-4 col-sm-6 mb-4">';
      card += '  <div class="card h-100">';
      card += '    <img src="' + item.image + '" class="card-img-top" alt="' + item.title + '">';
      card += '    <div class="card-body">';
      card += '      <h5 class="card-title truncate">' + item.title + '</h5>';
      card += '      <p class="card-text">';
      card += '        <span class="stock">' + item.category + '</span>';
      card += '      </p>';
      card += '    </div>';
      card += '  </div>';
      card += '</div>';

      $('#contenedor-productos').append(card);

    });

  });

});


$(document).ready(function() {
  $("#formprod").validate({
      rules: {
        productoId: {
          required: true,
        },
        nombre: {
          required: true,
        },
        descripcion: {
          required: true,
        },
        precio: {
          required: true,
        },
        imagen: {
          required: true,
        },
      }, // Fin de reglas
      messages: {
        productoId: {
          required: "Por favor ingresa una ID",
        },
        nombre: {
          required: "Por favor ingresa un nombre",
        },
        descripcion: {
          required: "Por favor ingresa una descripción",
        },
        precio: {
          required: "Por favor ingresa un precio",
        },
        imagen: {
          required: "Por favor ingresa una imagen",
        },
      },
    });
});


$(document).ready(function() {
  $("#formuser").validate({
      rules: {
        id: {
          required: true,
        },
        rut: {
          required: true,
          rutChileno: true,
        },
        nombres: {
          required: true,
        },
        apellidos: {
          required: true,
        },
        correo: {
          required: true,
          email: true,
        },
        direccion: {
          required: true,
        },
        password: {
          required: true,
          minlength: 6,
        },
        imagen: {
          required: true,
        }
      }, // Fin de reglas
      messages: {
        id: {
          required: "Por favor ingresa una ID",
        },
        rut: {
          required: "Por favor ingresa tu RUT",
        },
        nombres: {
          required: "Por favor ingresa un nombre",
        },
        apellidos: {
          required: "Por favor ingresa un apellido",
        },
        correo: {
          required: "Por favor ingresa un correo",
          email: "Por favor ingresa un correo válido",
        },
        direccion: {
          required: "Por favor ingresa una direccion",
        },
        password: {
          minlength: "La contraseña debe tener al menos 6 caracteres",
          required: "Por favor ingresa una contraseña",
        },
        imagen: {
          required: "Por favor ingresa una imagen",
        },
      },
    });
});






  $("#formmdatos").validate({
      rules:{
      inputNombres4: {
          required:true,
      },
      inputApellidos4: {
          required: true,
      },
      inputRut4: {
          required: true,
          rutChileno: true,
      },
      inputCorreo4: {
          required: true,
          email: true,
      },
      floatingTextarea2: {
          required: true,
      },
      inputContraseña1: {
          required: true,
          minlength: 6,
      },
      inputContraseña4: {
          required: true,
          equalTo: "#inputContraseña1",
      },
  },
  messages: {
      inputNombres4: {
          required: "Ingrese su Nombre",
      },
      inputApellidos4: {
          required: "Ingrese su Apellido",
      },
      inputRut4: {
          required: "Ingrese su Rut",
      },
      inputCorreo4:{
          required: "Ingrese su correo",
          email: "Ingrese un correo valido",
      },
      floatingTextarea2:{
          required: "Ingrese una Direccion valida",
      },
      inputContraseña1:{
          required: "Por favor ingresa una contraseña",
          minlength: "La contraseña debe tener al menos 6 caracteres",
      },
      inputContraseña4: {
          required: "Por favor confirma tu contraseña",
          equalTo: "Las contraseñas no coinciden",
      },
  },
  });
});
