from django.test import TestCase
from usuarios.forms import RegisterForm
from parameterized import parameterized

class UserRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username','Digite seu username. Ex:"user_name".'),
        ('email','Digite seu email. Ex:"user@email.com".'),
        ('telefone','Digite seu telefone. Ex:"ddd 9 9999-9999".'),
        ('password1','Senha:'),
        ('password2','Confirme sua senha:'),
    ])
    def test_placeholder_is_correct(self,field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder,placeholder)


    @parameterized.expand([
            ('username',''),
            ('email',''),
            ('telefone',''),
            ('password1',''),
            ('password2',''),
        ])
    def test_placeholder_is_correct(self,field, needed):
            form = RegisterForm()
            current = form[field].help_text
            self.assertEqual(current,needed)

     
    def test_validators_works_right(self):
         dados_validos = {
              'username':'usuario',
              'email':'emailcerto@hotmail.com',
              'telefone':'85996767696',
              'password1':'Suficiente1',
              'password2':'Suficiente1',
         }

         form = RegisterForm(data = dados_validos)


         self.assertTrue(form.is_valid())

    @parameterized.expand([
            ('email',''),
            ('password1','Senha deve ter: No mínimo 8 caracteres, letras maiúsculas, minúsculas e números. A senha e a confirmação devem ser iguais.'),
        ])
    def test_error_messages_and_validations_are_right(self,field,message):
         
        dados_invalidos = {
              'username':'usuario',
              'email':'emaielerrado',
              'telefone':'telefoneinvalido',
              'password1':'fraca',
              'password2':'fraca',
         }

        form = RegisterForm(data = dados_invalidos)

        self.assertFalse(form.is_valid())

        current_message = form.errors[field][0]
    
        
        self.assertEqual(current_message, message)