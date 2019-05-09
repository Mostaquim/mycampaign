var template_data = []
template_data['payment'] = '<p>Hi&nbsp;<br><br>We are currently awaiting your payment in order to progress your latest order. Please kindly clear the outstanding invoice in order to avoid any disruption with your distribution campaign.<br><br>Kind regards<br><br>Campaign Manager<br></p>';

var ParametrosButton = function (context) {

  var ui = $.summernote.ui;
  var list =  '<li data-template="payment" class="summernote-dropdown">Awaiting Payment</li>' + 
              '<li data-template="commence" class="summernote-dropdown">Notification of Campaign Commencement</li>' + 
              '<li data-template="suspense" class="summernote-dropdown">Notification of Campaign Suspension</li>' + 
              '<li data-template="hold" class="summernote-dropdown">Campaign on hold pending payment</li>' + 
              '<li data-template="delay" class="summernote-dropdown">Campaign Delay Notification</li>';

  var button = ui.buttonGroup([
      ui.button({
          className: 'dropdown-toggle',
          contents: '<span class="fa fa-database"></span> Templates <span class="caret"></span>',
          tooltip: "Parámetros disponibles",
          data: {
              toggle: 'dropdown'
          }
      }),
      ui.dropdown({
          className: 'summernote-list',
          contents: list,
          callback: function ($dropdown) {                    
              $dropdown.find('li').each(function () {
                var self = this
                  $(this).click(function () {                                                       
                      $('#summernote').summernote('reset');
                      $('#summernote').summernote('code', template_data[$(self).data('template')] );
                  });
              });
          }
      })
  ]);

  return button.render();   // return button as jquery object 
}

$(document).ready(function () {
  $('#summernote').summernote({
    toolbar: [
      ['style', [ 'bold', 'italic', 'underline', 'clear']],
      ['font', ['strikethrough', 'superscript', 'subscript']],
      ['para', ['ul', 'ol', 'paragraph']],
      ['view', ['templates','codeview']]
    ],
    buttons: {
      templates: ParametrosButton
    },
    popover: {
      image: [
        ['imagesize', ['imageSize100', 'imageSize50', 'imageSize25']],
        ['float', ['floatLeft', 'floatRight', 'floatNone']],
        ['remove', ['removeMedia']]
      ],
      link: [
        ['link', ['linkDialogShow', 'unlink']]
      ],
      air: [
        ['color', ['color']],
        ['font', ['bold', 'underline', 'clear']],
        ['para', ['ul', 'paragraph']],
        ['table', ['table']],
        ['insert', ['link', 'picture']]
      ]
    }
  });
});