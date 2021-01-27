$('body').on('click', 'input.delete_button', function() {
   $(this).parents('tr').remove();
});
