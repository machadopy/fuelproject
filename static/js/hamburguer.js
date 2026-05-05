const hamburguer = document.querySelector('.hamburguer');
const nav = document.querySelector('.navitens');

if (hamburguer && nav) {
	hamburguer.addEventListener('click', () => {
		nav.classList.toggle('active');
		hamburguer.classList.toggle('active');
	});
}