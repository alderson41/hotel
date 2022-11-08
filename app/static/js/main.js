function checkSession(){
    var session = window.localStorage.getItem('table_id')

    if (session == undefined || session == null){
        window.location = '/error'
    }
}


// change order status in user to preparing or completed
// render orders in the cook tab after responding to the order.