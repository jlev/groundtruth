<script charset="utf-8" type="text/javascript">
  $(function(){
    $("select#id_category").change(function(){
      $.getJSON("/db/",{id: $(this).val(), view: 'json'}, function(j) {
        var options = '<option value="">--------&nbsp;</option>';
        for (var i = 0; i < j.length; i++) {
          options += '<option value="' + j[i].optionValue + '">' + j[i].optionDisplay + '</option>';
        }
        $("#id_item").html(options);
        $("#id_item option:first").attr('selected', 'selected');
      })
      $("#id_category").attr('selected', 'selected');
    })
  })
</script>