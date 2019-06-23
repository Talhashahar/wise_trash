ENDPOINT = 'localhost:5000';


function change_bar(){
    var slider = document.getElementById("myRange");
    var output = document.getElementById("demo");
    output.innerHTML = slider.value;

    slider.oninput = function() {
      output.innerHTML = this.value;
    }

}
function zzz(){
    $(document).ready(function () {
  $('#table_calc').DataTable();
  $('.dataTables_length').addClass('bs-select');
});

$(document).ready(function () {
  $('#table_calc').DataTable({
    "paging": false // false to disable pagination (or any other option)
  });
  $('.dataTables_length').addClass('bs-select');
});
}

zzz();