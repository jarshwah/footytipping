Tipping = {
  configure: function(post_url) {
    $(document).ready(function attachSubmit() {
        $("form").each(function(idx, form) {
            $(form).submit(function(event) {
                $(form).siblings('span').html('');
                event.preventDefault();
                $.post(post_url, $(form).serialize())
                  .success(function(data, status, jqxhr) {
                    if (data.success) {
                        $(form)
                        .children('.button')
                          .addClass('selected')
                        .end()
                        .siblings('form')
                          .children('.button')
                            .removeClass('selected')
                          .end()
                        .end()
                        .siblings('span')
                          .removeClass('error')
                          .html('Tip Added');
                    } else {
                        $(form).siblings('span').addClass('error').html('Error Occurred');
                    }
                })
                .error(function(jqxhr, status, error) {
                  $(form).siblings('span').addClass('error').html("Error: " + error);
                });
            });
        });
    });
  }
};

