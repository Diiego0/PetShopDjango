
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




  $('#form').validate({ 
    rules: {
      'username': {
        required: true,
      },
      'first_name': {
        required: true,
      },
      'first_name': {
        required: true,
      },
      'last_name': {
        required: true,
      },
      'email': {
        required: true,
        email: true,
      },
      'rut': {
        required: true,
        rutChileno: true,
      },
      'direccion': {
        required: true,
      },
      'password1': {
        required: true,
        minlength: 8,
      },
      'password2': {
        required: true,
        equalTo: '#id_password1'
      }
    },
    messages: {
      'username': {
        required: 'Debe ingresar un nombre de usuario',
      },
      'first_name': {
        required: 'Debe ingresar su nombre',
      },
      'last_name': {
        required: 'Debe ingresar sus apellidos',
      },
      'email': {
        required: 'Debe ingresar su correo',
        email: 'El formato del correo no es válido',
      },
      'rut': {
        required: 'Debe ingresar su RUT',
        rutChileno: 'El formato del RUT no es válido',
      },
      'direccion': {
        required: 'Debe ingresar su dirección',
      },
      'password1': {
        required: 'Debe ingresar una contraseña',
        minlength: 'La contraseña debe tener al menos 8 caracteres',
      },
      'password2': {
        required: 'Debe ingresar una contraseña',
        equalTo: 'Debe repetir la contraseña anterior'
      }
    },
    errorPlacement: function(error, element) {
      error.insertAfter(element); // Inserta el mensaje de error después del elemento
      error.addClass('error-message'); // Aplica una clase al mensaje de error
      //element.after('<br>'); 
    },
});






$('#id_imagen').change(function() {
  var input = this;
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function(e) {
      $('#registrarme-imagen').attr('src', e.target.result).show();
    };
    reader.readAsDataURL(input.files[0]);
  }
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
        idProducto: {
          required: true,
        },
        nombreProducto: {
          required: true,
        },
        descripcionProducto: {
          required: true,
        },
        precioProducto: {
          required: true,
        },
        imagenProducto: {
          required: true,
        },
      }, // Fin de reglas
      messages: {
        idProducto: {
          required: "Por favor ingresa una ID",
        },
        nombreProducto: {
          required: "Por favor ingresa un nombre",
        },
        descripcionProducto: {
          required: "Por favor ingresa una descripción",
        },
        precioProducto: {
          required: "Por favor ingresa un precio",
        },
        imagenProducto: {
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
        first_name: {
          required: true,
        },
        last_name: {
          required: true,
        },
        email: {
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
        first_name: {
          required: "Por favor ingresa un nombre",
        },
        last_name: {
          required: "Por favor ingresa un apellido",
        },
        email: {
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
      },
  },
  });
});
