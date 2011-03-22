$('.petPag').click(function(){
	$('.petPag > a').fadeOut();
	$('.petPag').html('<img src="images/ajax-loader.gif" alt="Loading..." />');
	var offset = $('.pet').length;
	var address = '/svc/adoptions/' + offset + '.html';
	$.ajax({
		url: address,
		success: function(results){
			$('.petPag > img').fadeOut();
			$('.petPag').html('<a href="#">See More Pets!</a>').hide().fadeIn(400);
			$('#availablePets').append(results).stop().hide().slideDown(400);
		}
	});	
	return false;
});



