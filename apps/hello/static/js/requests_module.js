var CORE, REQTABLE, PAGEHEHEADUPDATE, AJAXREQ;
CORE = (function(){
    var moduleData = {};
    return{
        //Register module in CORE, to add it to moduleData object
        registerModule: function(moduleName, that){
            moduleData[moduleName] = {
                modObj : that,
                status : null
            };
        },
        //Init all modules consist in moduleData
        startAllMod: function(){
            for (var mod in moduleData){
                if (moduleData.hasOwnProperty(mod)) {
                    moduleData[mod].modObj.init();
                    console.log('init', mod);
                }
            }
        },
        //Register module-observer at the event of module-publisher
        registerEvents: function(moduleName, evts){
            moduleData[moduleName].events = evts;
        },
		//Triger some event
        triggerEvent: function(evt){
            for (var mod in moduleData){
                if (moduleData.hasOwnProperty(mod)){
                    mod = moduleData[mod];
                    if (mod.events && mod.events[evt.type]){
                        mod.events[evt.type](evt.data);
                    }
                }
            }
        }
    };
})();

REQTABLE = (function(){
    var moduleName = 'REQTABLE',
        that,
        reqViewedStatus; //Status - all new requests is viewed
    //Private help method, cloning tr elements from table in DOM
    function cloneDomTrEls(){
        var $trEls;
        $trEls = $('tr', '#requests_table_content').clone();
        return $trEls
    }
    //Private help method, removing 'NEW' from td elements
    function removeNewStatus(i, $trEls){
        var newTdEl;
        newTdEl = $trEls[i].getElementsByTagName('td')[5];
        if(newTdEl){
			newTdEl.innerHTML = ''
        }
        return false
    }
    //Private help metod, inserting edit collections of td elements in DOM
    function insertNewReqTable($trEls){
        var $inserTable,
            $domReqTable;
        $inserTable = $('<tbody id="requests_table_content"></tbody>');
        $inserTable.append($trEls);
        $domReqTable = $('#requests_table_content');
        if(!$domReqTable.length){
            $domReqTable = $('#no_requests_table')
        }
        $domReqTable.replaceWith($inserTable);
        return false
    }
    return{
        coreRegister: function(){
            CORE.registerModule(moduleName, this);
            return false
        },
        init: function(){
			var $reqTable;
            that = this;
			$reqTable = $('#requests_table');
            $reqTable.on('mouseenter', this.removeAllNewStatus);
            reqViewedStatus = false;
            return false
        },
        //Facade public method removing all 'NEW' from DOM
        removeAllNewStatus: function(){
            var $trEls;
            $trEls = cloneDomTrEls();
            if($trEls.length&&reqViewedStatus==false){
                for(var i= 0, max = $trEls.length; i < max; i++){
                    removeNewStatus(i, $trEls)
                }
                insertNewReqTable($trEls);
                CORE.triggerEvent({
                    type: 'removeAllNewStatus'
                });
                reqViewedStatus = true
            }
        }
    };
}());
REQTABLE.coreRegister();

AJAXREQ = (function(){
    var that,
        moduleName = 'AJAXREQ',
        ajaxReqPollingInterval;
    return{
        coreRegister: function() {
            CORE.registerModule(moduleName, this);
        },
        init: function(){
            var $lastRequestTime;
            that = this;
            sessionStorage["lastRequestTime"] = '';
            $lastRequestTime = $('#last_request_time');
            if ($lastRequestTime.length) {
                sessionStorage["lastRequestTime"] = $lastRequestTime.text();
            }
            this.startGetAjaxReqPolling();
        },
		//Start ajax requests polling via seInterval function
        startGetAjaxReqPolling: function(){
            if(ajaxReqPollingInterval==null){
                ajaxReqPollingInterval = setInterval(function(){
                var ajaxRequestData = {};
                ajaxRequestData['last_request_time'] = sessionStorage["lastRequestTime"];
                //$.get('/requests/', ajaxRequestData).done(that.handleGetAjaxReqPoll)
            }, 4000)
            }
        },
		//Handle ajax response data, running helper method and trigger newAjaxRespPoll event
        handleGetAjaxReqPoll: function(ajaxReqArr){
            var $reqTrEls;
            if(ajaxReqArr.length) {
				//handle ajaxReqArr
            }
        },
        //Stop ajax requests polling interval
        stopGetAjaxReqPolling: function(){
            if(ajaxReqPollingInterval!=null){
                clearInterval(ajaxReqPollingInterval)
            }
            ajaxReqPollingInterval = null
        }
    };
})();
AJAXREQ.coreRegister();

PAGEHEHEADUPDATE = (function(){
    var moduleName = 'PAGEHEHEADUPDATE',
		newStatus, //'NEW' counter for page header
        that;
    return{
        coreRegister: function() {
            CORE.registerModule(moduleName, this);
        },
        init: function(){
            that = this;
            newStatus = 0;
            CORE.registerEvents(moduleName,{
                'removeAllNewStatus': this.resetPageHeader
            });
        },
		//Reset page title after removing all 'NEW' status
        resetPageHeader: function(){
           newStatus = 0;
           $('title').replaceWith('<title>('+newStatus+') new requests</title>')
        }
    };
})();
PAGEHEHEADUPDATE.coreRegister();

CORE.startAllMod()
