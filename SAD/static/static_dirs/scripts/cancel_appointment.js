function clicked(e, usr, evt) {
    var r = confirm('آیا از لغو ویزیت اطمینان دارید؟\n *10 درصد از مبلغ بازگشت پذیر نیست.*');
    if (r === true) {
        $.ajax({
            url: "cancel/" + usr.toString() + "/" + evt.toString(),

        });
        window.location.reload();
    } else {
        e.preventDefault();

    }
}



