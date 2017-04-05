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
	//Private help method, unit new tr element collections with DOM one
    function unitTrEls($trEls, $reqTrEls){
        $trEls = $reqTrEls.add($trEls);
        if($trEls.length > 10){
            $trEls = $trEls.slice(0, 10)
        }
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
    function updateTabNum(i, $trEls){
        var numStr, num;
        $trEls[i].getElementsByTagName('td')[0].remove();
        num = i+1;
        numStr = '<td>'+num+'</td>';
        $trEls[i].insertAdjacentHTML('afterBegin', numStr);
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
			CORE.registerEvents(moduleName, {
                'newAjaxRespPoll': this.addNewRequests
            });
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
        },
		//Facade ppublic method insrt new tr elements collections to DOM
        addNewRequests: function($reqTrEls){
            var $trEls;
            $trEls = cloneDomTrEls();
            if($trEls.length){
                $trEls = unitTrEls($trEls, $reqTrEls)
            }else{
                $trEls = $reqTrEls
            }
            for(var i= 0, max = $trEls.length; i < max; i++){
                updateTabNum(i, $trEls);
            }
            insertNewReqTable($trEls);
            reqViewedStatus = false;
        },
    };
}());
REQTABLE.coreRegister();

AJAXREQ = (function(){
    var that,
        moduleName = 'AJAXREQ',
        ajaxReqPollingInterval;
	//Create data array to mock response from server 
	function getMockAjaxData(){
		var ajaxReqArr,
			reqObj,
			objNum;
		ajaxReqArr = [];
		reqObj = {
			id: 0,
			method: "GET",
			path: "/requests/",
			request_time: "2017-04-05T07:33:37",
			status_code: 200
		};
		
		objNum = Math.floor(Math.random() * (4));
		for(var i= 0; i < objNum; i++){
			ajaxReqArr.push(reqObj)
		}
		return ajaxReqArr
	}
	//Private helper method take JSON data from server 
	//return tr elements collections to insert in requests table
    function getReqTrEls(ajaxReqArr){
        var reqTrArr,
            $reqTrEls,
            reqTrHtml;
        newCount = 0;
        $reqTrEls = $();
        for (var i=0; i<ajaxReqArr.length; i++) {
			newCount += 1;
            reqTrArr = [
                +i + 1,
                ajaxReqArr[i].request_time,
                ajaxReqArr[i].path,
                ajaxReqArr[i]['status_code'],
                ajaxReqArr[i]['method'],
                'NEW'
            ];
            reqTrHtml = '<tr><td>' + reqTrArr.join('</td><td>') + '</td></tr>';
            $reqTrEls = $reqTrEls.add(reqTrHtml);
        }
        return $reqTrEls
    }
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
			var ajaxReqArr;
            if(ajaxReqPollingInterval==null){
                ajaxReqPollingInterval = setInterval(function(){
                var ajaxRequestData = {};
                ajaxRequestData['last_request_time'] = sessionStorage["lastRequestTime"];
                //$.get('/requests/', ajaxRequestData).done(that.handleGetAjaxReqPoll)
				ajaxReqArr = getMockAjaxData();
				that.handleGetAjaxReqPoll(ajaxReqArr)
            }, 4000)
            }
        },
		//Handle ajax response data, running helper method and trigger newAjaxRespPoll event
        handleGetAjaxReqPoll: function(ajaxReqArr){
            var $reqTrEls;
            if(ajaxReqArr.length) {
				$reqTrEls = getReqTrEls(ajaxReqArr);
				CORE.triggerEvent({
                    type: 'newAjaxRespPoll',
                    data: $reqTrEls
                })
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
