$('.petPag').click(function(){
	var offset = $('.pet').length;
	var address = '/svc/adoptions/' + offset + '.html';
	$('.petPag > a').fadeOut();
	$('.petPag').html('<img src="images/ajax-loader.gif" alt="Loading..." />');
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



