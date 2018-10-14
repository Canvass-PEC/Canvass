$(function () {
  $(".publish").click(function () {
    $("input[name='status']").val("P");
    $("form").submit();
  });

  $(".draft").click(function () {
    $("input[name='status']").val("D");
    $("form").submit();
  });

  $(".preview").click(function () {
    $.ajax({
      url: '/articles/preview/',
      data: $("form").serialize(),
      cache: false,
      type: 'post',
      beforeSend: function () {
        $("#preview .modal-body").html("<div style='text-align: center; padding-top: 1em'><img src='/static/img/loading.gif'></div>");
      },
      success: function (data) {
        $("#preview .modal-body").html(data);
      }
    });
  });

  $("#comment").focus(function () {
    $(this).attr("rows", "3");
    $("#comment-helper").fadeIn();
  });

  $("#comment").blur(function () {
    $(this).attr("rows", "1");
    $("#comment-helper").fadeOut();
  });

  $("#comment").keydown(function (evt) {
    var keyCode = evt.which?evt.which:evt.keyCode;
    if (evt.ctrlKey && (keyCode == 10 || keyCode == 13)) {
      $.ajax({
        url: '/articles/comment',
        data: $("#comment-form").serialize(),
        cache: false,
        type: 'post',
        success: function (data) {
          $("#comment-list").html(data);
          var comment_count = $("#comment-list .comment").length;
          $(".comment-count").text(comment_count);
          $("#comment").val("");
          $("#comment").blur();
        }
      });
    }
  });


$(".vote").on("click",function () {
    var span = $(this);
    var article=$("input[name='qid']").val();
    var csrf = $("input[name='csrfmiddlewaretoken']").val();
    var vote = "";
    if ($(this).hasClass("voted")) {
      var vote = "R";
    }
    else if ($(this).hasClass("up-vote")) {
      vote = "V";
    }
    else if ($(this).hasClass("down-vote")) {
      vote = "E";

    }
    $.ajax({
      url: '/articles/vote',
      data: {
        'article': article,
        'vote': vote,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
      success: function (data) {
        var options = $(span).closest('.options');
        $('.vote', options).removeClass('voted');
        if (vote == 'V' || vote == 'E') {
          $(span).addClass('voted');
          var text=$(span).text();
          if(text=="Upvote")
          {
            $(span).text("Upvoted");
            $(span).next().text("Downvote");
          }
          else if(text=="Downvote")
          {
            $(span).text("Downvoted");
            $(span).prev().text("Upvote");
          }
        }
        else{
         var text=$(span).text();
          if(text=="Upvoted")
            {
                $(span).text("Upvote");
                $(".upvotes > span").first().text(val);
                $(".upvote").text(val);
            }
          else
                $(span).text("Downvote");
                $(".downvotes > span").first().text(val);
                $(".downvote").text(val);
        }
      }
    });
  });
});