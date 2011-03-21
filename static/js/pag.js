$('.petPag > a').click(function(){
	
	var offset = $('.pet').length;
	var address = '/svc/adoptions/' + offset + '.html';

	$.ajax({
		url: address,
		success: function(results){
			 $('#availablePets').append(results).hide().fadeIn(400);
		}
	});	
	return false;

});



