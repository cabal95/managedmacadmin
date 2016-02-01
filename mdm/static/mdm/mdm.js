(function ($) {
  $.fn.editable = function(fnSave, fnValidate, fnFormat) {
    var content = $('<span class="editableContent"></span>').text($(this).text());
    var edit = $('<i style="font-size: 14px;" class="fa fa-edit"></i>');

    if (typeof(fnSave) === 'undefined')
      fnSave = function (object, value, done) { done(true); };
    if (typeof(fnValidate) === 'undefined')
      fnValidate = function (object, value) {
        if ($(object).data('required') == true && value.length == 0) {
          alert('Value is required.');
          return false;
        }
        return true;
      };

    if ($(content).text().length == 0)
      $(this).addClass('empty');
    else
      $(this).removeClass('empty');

    $(this).text('');
    $(this).append(content).append(edit);

    $(edit).click(function () {
      var src = $(this).prevAll('.editableContent').first();
      var tb = $('<input type="text" class="editing"></input>');
      var save = $('<button type="text" class="saveButton btn btn-primary has-spinner"><span class="spinner"><i class="fa fa-refresh fa-spin" style="margin-right: 5px;"></i></span><i class="icon-ok"></i></button>');
      var cancel = $('<button type="text" class="cancelButton btn btn-warning"><i class="icon-remove"></i></button>');
      var width = $(src).width();

      $(tb).val($(src).text());
      $(this).parent().append(tb).append(save).append(cancel);
      $(src).hide();
      $(this).css('display', 'none');
      width -= $(save).outerWidth();
      width -= $(cancel).outerWidth();
      if (width < 100)
        width = 100;
      $(tb).css('width', width + 'px');
      $(tb).select();
      $(tb).focus();

      $(tb).keyup(function (e) {
        if (e.keyCode == 13) {
          e.preventDefault();
          $(save).click();
        }
        if (e.keyCode == 27) {
          e.preventDefault();
          $(cancel).click();
        }
      });

      $(save).click(function () {
        var tb = $(this).prevAll('.editing').first();
        var save = $(this);
        var cancel = $(this).next('.cancelButton').first();
        var orig = $(this).prevAll('.editableContent').first();
        var container = $(this).parent('.editable').first();
        var icon = $(this).prevAll('.fa-edit');
        var value = $(tb).val();

        var done = function (ok) {
          if (ok === true) {
            $(orig).text(value);
            $(orig).show();
            $(icon).css('display', '');
            $(tb).remove();
            $(save).remove();
            $(cancel).remove();

            if (value.length == 0)
              $(container).addClass('empty');
            else
              $(container).removeClass('empty');
          }
          else
            $(save).removeClass('active');
        };

        if (fnValidate($(orig).parent(), value) === false) {
          $(tb).focus();
          return;
        }

        $(save).addClass('active');
        fnSave($(orig).parent(), value, done);
      });

      $(cancel).click(function () {
        var tb = $(this).prevAll('.editing').first();
        var save = $(this).prevAll('.saveButton').first();
        var cancel = $(this);
        var orig = $(this).prevAll('.editableContent').first();
        var icon = $(this).prevAll('.fa-edit');

        $(orig).show();
        $(icon).css('display', '');
        $(tb).remove();
        $(save).remove();
        $(cancel).remove();
      });
    });
  };

  /*
   * Selected elements become fancy two-stage delete buttons.
   */
  $.fn.deleteButton = function(fnDelete) {
    if ($(this).length > 1) {
      $(this).each(function() { $(this).deleteButton(fnDelete); });
      return $(this);
    }

    var expandButton = function(e) {
      var btn = $(this);
      var origContent = $(btn).html();
      var origWidth = $(btn).outerWidth(), origHeight = $(btn).outerHeight();
      var width, height;

      $(btn).unbind("click.ExpandDelete");
      $(btn).bind("click.DoDelete", fnDelete);
      $(btn).html(origContent + ' Delete');
      width = $(btn).outerWidth();
      height = $(btn).outerHeight();
      $(btn).html(origContent);
      $(btn).css('visibility', 'visible');
      $(btn).css('text-align', 'left');
      $(btn).css('width', origWidth);
      $(btn).css('height', origHeight);
      $(btn).animate({ width: width, height: height }, 100, function() {
        $(btn).html(origContent + ' Delete');
      });                                         

      e.stopPropagation();

      $(document).bind("click.ClearDelete", function (e) {
        if ($(btn).has(e.target).length > 0 || e.target == $(btn).get(0))
          return;
        $(btn).unbind("click.DoDelete");
        $(document).unbind("click.ClearDelete");
        $(btn).html($(btn).html().replace(' Delete', ''));
        $(btn).animate({ width: origWidth, height: origHeight }, 100, function() {
          $(btn).css('width', '').css('height', '');
          $(btn).css('visibility', '');
          $(this).bind("click.ExpandDelete", expandButton);
        });
      });
    };

    $(this).bind("click.ExpandDelete", expandButton);
  };
})(jQuery);
