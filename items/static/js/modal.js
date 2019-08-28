$(document).ready(function() {
	/* Store elements:
		modal:the modal;
		closeModal: the modal button (cancel) to close the modal;
		triggers: the links that trigger the modal;
		login, signup: the other buttons (links) in the modal;
		loginHref, signupHref: the hrefs of login and signup.
		*/
    const   modal = document.getElementById('modal'),
			closeModal = document.getElementById('close-modal'),
			triggers = document.getElementsByClassName('loginRequired'),
		  	login = document.getElementById('login'),
		  	signup = document.getElementById('signup'),
		  	loginHref = login.getAttribute('href'),
		  	signupHref = signup.getAttribute('href');
	
	/*
	On each trigger (.loginRequired), add an event listener that:
	prevents going to the link destination;
	gets the href of the clicked element and concatenates it to '?next=' to create a next GET parameter;
	appends the former to the current href of both buttons (links) in modal;
	triggers the modal by removing the closed class;
	pauses the slider (#imgcarousel).
	*/
	for (let trigger of triggers) {
		trigger.addEventListener('click', (e) => {
			e.preventDefault();
			let next = '?next=' + e.target.getAttribute('href');
			
			login.setAttribute('href', loginHref + next);
			signup.setAttribute('href', signupHref + next);
			modal.classList.remove('closed');
			$('#imgcarousel').carousel('pause');
		});
	}
	/*
	Clicking the modal's Cancel button will:
	close the modal by adding the closed class to it;
	reset the hrefs of modal's login and signup buttons (links);
	re-start the slider.
	*/
	closeModal.addEventListener('click', () => {
		modal.classList.add('closed');
		$('#imgcarousel').carousel('cycle');
		login.setAttribute('href', loginHref);
		signup.setAttribute('href', signupHref);
		}
	);
	//Same thing when pressing esc while modal is open.
	document.addEventListener('keyup', (e) => {
		let key = e.key || e.keyCode;
		if (!modal.classList.contains('closed') && (key === 'Escape' || key === 'Esc' || key === 27)){
			modal.classList.add('closed');
			$('#imgcarousel').carousel('cycle');
			login.setAttribute('href', loginHref);
			signup.setAttribute('href', signupHref);
			}
	});
});