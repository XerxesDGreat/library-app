function initAutocomplete(textFieldName, url) {
    $('#' + textFieldName + '_autocomplete').autocomplete({
        source: url,
        minLength: 2,
        select: function (event, ui) {
            $('#' + textFieldName + '_autocomplete_id').val(ui.item.id);
        }
    });
}