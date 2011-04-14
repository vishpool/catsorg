$('.petPag').click(function(){
	var offset = $('#availablePets .pet').length;
	var address = '/svc/adoptions/' + offset + '.html';
	$('.petPag > a').fadeOut();
	$('.petPag').html('<img src="images/ajax-loader.gif" alt="Loading..." />');
	$.ajax({
		url: address,
		success: function(results){
			$('.petPag > img').fadeOut(100);
			$('.petPag').html('<a href="#">See More Pets!</a>');
			$('#availablePets').append(results);
			$('html, body').animate({scrollTop: $('#pag' + offset).offset().top}, 'slow');
		},
	});	
	return false;
});



