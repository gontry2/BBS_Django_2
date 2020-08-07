var blockContent = "{% bootstrap_form comments_form%}";


$("#like").click(function(){
    var pk = $(this).attr('name')
    $.ajax({
      type: "GET",
      url: "/board/article/" + pk + "/like/",
      data: {'article_id': pk},
      dataType: "json",
      success: function(response){
        $("#id_like_num").text(response.like_num)
      },
      error: function(request, status, error){
        console.log(error)
      },
    });
  })

$("#unlike").click(function(){
    var pk = $(this).attr('name')
    $.ajax({
      type: "GET",
      url: "/board/article/" + pk + "/unlike/",
      data: {'article_id': pk },
      dataType: "json",
      success: function(response){
        $("#id_unlike_num").text(response.unlike_num)
      },
      error: function(request, status, error){
        console.log(error)
      },
    });
  })

$("#comments_form").submit(function(event){
 console.log("click");
    event.preventDefault();
    if ($("#id_comment").val() === '') {
        alert('댓글 내용을 입력하세요');
    } else {
        var pk = $(this).attr('name')
        $.ajax({
          type: "POST",
          url: "/board/article/" + pk + "/addComment/",
          data: $("#comments_form").serialize(),
          contentType: "application/x-www-form-urlencoded;charset=utf-8",
          dataType: "json",
          async: false,
          success: function(response){
            $("#comments_list").append(
            "<tbody id=\"comment_" + response.comment_id + "\" name='comment_id'><tr><td>" + response.comment + "</td><td><a class=\"deleteComment\" name='" + response.comment_id + "'><img src=\"https://img.icons8.com/officexs/16/000000/delete-sign.png\"/></a></td>"
            +"</tr><tr><td><img src=\"/static/image/person.png\"/>"+ response.writer + "</td><td><img src=\"https://img.icons8.com/material-two-tone/24/000000/date-to.png\"/>"
            + response.write_date + "</td></tr></tbody>"
            )
            $("#id_comment").val("")
          },
          error: function(request, status, error){
            console.log(error)
          },
        });
    }
  })

$(".comment").delegate(".deleteComment", "click", function(){
    console.log("click");
    var pk = $(this).attr('name')
    $.ajax({
      type: "GET",
      url: "/board/article/" + pk + "/deleteComment/",
      data: {'comment_id': pk },
      dataType: "json",
      async: false,
      success: function(response){
        console.log(response)
        $("#comment_"+response.comment_id).remove();
        console.log("성공")
      },
      error: function(request, status, error){
        console.log(error)
      },
    });
  })


//  $("#comment_reply").click(function(){
//  event.preventDefault();
//    console.log('reply');
//    var pk = $(this).attr('name')
//    console.log($("#comment_"+pk))
//
//    $("#comment_"+pk).append(blockContent)
//
//  })