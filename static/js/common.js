$('.ui.dropdown').dropdown();
$(document).ready(function() {
  $("#searchIcon").click(function() {
    $("#searchForm").submit();
  });
});

$(document).ready(function(){
  $('.products').slick({
    dots: true,
    infinite: false,
    arrows: true,
    speed: 300,
    slidesToShow: 5,
    slidesToScroll: 5,
  });
});