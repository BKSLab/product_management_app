$('#add_product_to_warehouse').on('show.bs.modal', function (e) {
  var dataId = $(e.relatedTarget).data('id');
  $(this).find('input.hidden-input').val(dataId);
});

$('#del_product_to_warehouse').on('show.bs.modal', function (e) {
  var dataInfo = $(e.relatedTarget).data('info');
  $(this).find('input.hidden-input').val(dataInfo);
});

$('#change_quantity_products').on('show.bs.modal', function (e) {
  var dataInfo = $(e.relatedTarget).data('info');
  $(this).find('input.hidden-input').val(dataInfo);
});
