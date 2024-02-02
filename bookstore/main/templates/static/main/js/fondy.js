var checkoutStyles = {
    'html , body' : {
        'overflow' : 'hidden'
    },
    '.input_suggest .arrow' : {
        'display' : 'none'
    },
    '[name="card_number"]' : {
        'width' : '320px !important'
    },
    '.pages-checkout .page-section-shopinfo' : {
        'background' : 'transparent'
    },
    '.col.col-shoplogo' : {
        'display' : 'none'
    },
    '.col.col-language' : {
        'display' : 'none'
    },
    '.pages-checkout' : {
        'background' : 'transparent'
    },
    '.col.col-login' : {
        'display' : 'none'
    },
    '.pages-checkout .page-section-overview' : {
        'background' : '#fff',
        'color' : '#252525',
        'border-bottom' : '1px solid #dfdfdf'
    },
    '.col.col-value.order-content' : {
        'color' : '#252525'
    },
    '.page-section-footer' : {
        'display' : 'none'
    },
    '.page-section-tabs' : {
        'display' : 'none'
    },
    '.btn-row' : {
        'margin' : '20px'
    },
    '#submit_button_row' : {
        'display': 'none'
    },
    '.btn-block' : {
        'font-size' : '18px',
        'line-height' : '50px',
    }
};

function __DEFAULTCALLBACK__(data,type){
    var form;
    console.log('action',data.action);
    console.log('url',data.url)
    for(var prop in data.send_data){
        if(data.send_data.hasOwnProperty(prop)){
            console.log(prop,data.send_data[prop]);
        }
    }
    if ( data.error){
        console.log(data,data.error);
        return;
    }
    if (data.action == 'redirect') {
        this.loadUrl(data.url);
        return;
    }
    if (data.send_data.order_status == 'delayed') {
        this.unbind('ready');
        this.hide();
        return;
    } else {
        this.unbind('ready').action('ready', function() {
            this.show();
        });
    }
    if( data.send_data && data.url ){
        form = prepareFormData(data.url,data.send_data);
        this.find('body').appendChild(form);
        form.submit();
        form.parentNode.removeChild(form);
    }
}

function checkoutInit(url){
    $ipsp('checkout').scope(function(){
        this.setCheckoutWrapper('#checkout_wrapper');
        this.addCallback(__DEFAULTCALLBACK__);
        this.setModal(false);
        this.setCssStyle(checkoutStyles);
        this.action('show', function(data) {
            $('#checkout_loader').remove();
            $('#checkout').show();
        });
        this.action('hide', function(data) {
            $('#checkout').hide();
        });
        this.action('resize', function(data) {
            $('#checkout_wrapper').height(data.height);
        });            
        this.loadUrl(url);
    });
};

var button = $ipsp.get('button');
button.setMerchantId(1396424);
button.setAmount(2999.99,'USD',true);
button.setResponseUrl('http://shop.com/response/');
button.setHost('api.fondy.eu');
button.addField({
    label:'Product Description',
    name:'descr',
    value:'Apple MacBook Pro Retina Display',
    readonly:true
});    
button.addField({
    label:'Full Name',
    name:'username',
    value:'',
    required:true,
    placeholder:'Enter Your Name',
    valid:{
        'pattern':'^[a-zA-Z\s]+$'
    }
});
button.addParam('order_id','shop_order_'+Math.round(Math.random()*1000000));
//setTimeout(function(){
    $('#checkout_loader').append(button.getButton('Open checkout in new window','','_blank'));    
//},1600);
checkoutInit(button.getUrl());