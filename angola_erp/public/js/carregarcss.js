function carregar() {

	console.log('Carregar')
	if (frappe.session.user != undefined){
		css_file_user = './assets/angola_erp/css/erpnext/' + frappe.session.user + '_bootstrap.css'
		$.ajax({
			cache: false,
			url: css_file_user,
			type: 'HEAD',
			beforeSend: function() {
				console.log('antes de enviar')

			},
			success: function(data, textStatus, request){
				console.log(request.getResponseHeader('Header'))	
				console.log('ficheiro existe ', css_file_user);
				console.log($.ajax.arguments)
				console.log(textStatus)
				var dd = document.createElement('link')
				//dd.setAttribute('rel','preload')
				dd.setAttribute('rel','stylesheet')
				//dd.setAttribute('as','style')
				//dd.setAttribute('onload',"this.rel='stylesheet'")
				dd.setAttribute('type','text/css')

				console.log('assets/angola_erp/css/erpnext/' + frappe.session.user + '_bootstrap.css?ver={{ build_version }}')
				// http://192.168.229.146:8000/assets/angola_erp/css/angola_erp.css?ver=1510070115.0	/ ?ver=1510106168.0
				dd.setAttribute('href','assets/angola_erp/css/erpnext/' + frappe.session.user + '_bootstrap.css?reload=' + new Date().getTime())
				 //?ver=1510070115.0')

//				dd.onload = function(){
//					console.log('CARREGOU o ....');
//				};

				document.getElementsByTagName('head')[0].appendChild(dd);

			},
			error: function(resp){
				console.log('nao existe ...', resp)
			},
		})


	}
	
	
}


