function my_scope(){
    const form = document.querySelector('.form-delete')

    if (form ){
        form.addEventListener('submit', function (e){

            e.preventDefault();

            const confirmed = confirm ('Tem certeza que deseja excluir?');
            
            if (confirmed){
                form.submit();
            }
        });
    }
}
my_scope()