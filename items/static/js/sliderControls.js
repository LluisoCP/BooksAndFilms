jQuery(document).ready(function($) {
	$('#prevCarousel').click(() => { $('.carousel').carousel('prev') });
	$('#pauseCarousel').click(() => { $('.carousel').carousel('pause') });
	$('#playCarousel').click(() => { $('.carousel').carousel('cycle') });
	$('#nextCarousel').click(() => { $('.carousel').carousel('next') });
})