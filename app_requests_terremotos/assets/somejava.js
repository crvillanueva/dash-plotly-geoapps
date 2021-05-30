const tabla = document.querySelector('#tabla');

const boton_ocultar_tabla = document.querySelector('.btn-hide');

boton_ocultar_tabla.addEventListener('click', () => {
	tabla.style.width = "0";
	console.log('clicked')
})

alert('If you see this alert, then your custom JavaScript script has run!')
