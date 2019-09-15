jQuery(document).ready(function($) {
	setTimeout(() => $('#has-commented').removeClass('out'), 500);
	$('#close-commented').click(function() {
		$('#has-commented').addClass('out');
	})
	$(document).keyup(function(e) {
    	if (e.which === 27) {
			$('#has-commented').addClass('out');
    	}
	});
});