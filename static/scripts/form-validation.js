// function validateForm() {
//   if (
//     document.forms['my-form']['name'].value == '' ||
//     document.forms['my-form']['email'].value == '' ||
//     document.forms['my-form']['message'].value == ''
//   ) {
//     alert('Please fill out all fields.')
//     return false
//   }

//   var form = document.getElementById('form')
//   var form_response = document.getElementById('form-response')
//   var submit = document.getElementById('submit')
//   if (form.style.display === 'none') {
//     form.style.display = 'block'
//   } else {
//     form.style.display = 'none'
//     form_response.style.display
//     form_response.style.display = 'block'
//     submit.style.display = 'none'
//   }
//   return false
// }

$(function () {
  var a
  $("form[name='my-form']").validate({
    rules: {
      email: {
        required: true,
        email: true,
      },
      name: {
        required: true,
        minlength: 6,
      },
      message: {
        required: true,
        minlength: 10,
      },
    },
    messages: {
      name: {
        required: 'Please provide your name',
        minlength: 'Your name must be at least 6 characters long',
      },
      email: 'Please enter a valid email address',
      message: {
        required: 'Please provide your message',
        minlength: 'Your message must be at least 10 characters long',
      },
    },

    submitHandler: function (form) {
      a = true
      return false
    },
  })

  $('#submit').click(function () {
    setTimeout(function () {
      var name = $('#name').val()
      var response_message =
        'Hello Foodie, </br> </br> Thanks for submitting your query, we will get back to you shortly. </br> </br> - Admin (MyRecipeBook)'
      $('#form-response').html($.parseHTML(response_message))
      a &&
        $('#form').hide() &&
        $('#submit').hide() &&
        $('#form-response').show()
    }, 2000)
  })
})
