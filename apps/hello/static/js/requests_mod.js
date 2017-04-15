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
        newCount,
        reqViewedStatus;  //flag - all new requests are viewed
    //Private help method, cloning tr elements from table in DOM
    function cloneDomTrEls(){
        var $tbodyContent,
            $trEls;
        $tbodyContent = $("#requests_table_content");
        if($tbodyContent.length){
            $trEls = $('tr', '#requests_table_content').clone();
        }else{
            $trEls = $()
        }
        return $trEls
    }
    //Private help method, removing 'NEW' from td elements
    function initRemoveNewStatus($trEls, lastViewedReq) {
        var timeTdEl,
            newTdEl;
        for (var i = 0, max = $trEls.length; i < max; i++) {
            timeTdEl = $trEls[i].getElementsByTagName('td')[1].innerHTML;
            newTdEl = $trEls[i].getElementsByTagName('td')[5];
            //check if newTdEl is present in DOM ReqTable
            if (newTdEl) {
                if (timeTdEl <= lastViewedReq) {
                    newTdEl.innerHTML = ''
                } else {
                    newCount += 1;
                }
            }
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

    /**
     * Delete all NEW status in requests table
     * @param lastViewedReqTime
     */
    function removeAllNewStatus(lastViewedReqTime){
        var $trEls,
            lastViewedReq,
            timeTdEl,
            newTdEl;
        $trEls = cloneDomTrEls();
        if($trEls.length){
            lastViewedReqTime = $trEls[0].getElementsByTagName('td')[1].innerHTML;
            for (var i = 0, max = $trEls.length; i < max; i++) {
                timeTdEl = $trEls[i].getElementsByTagName('td')[1].innerHTML;
                newTdEl = $trEls[i].getElementsByTagName('td')[5];
                if(timeTdEl>lastViewedReqTime){
                    lastViewedReqTime = timeTdEl
                }
                if (newTdEl) {
                    newTdEl.innerHTML = ''
                }
            }
            console.log(lastViewedReqTime);
            insertNewReqTable($trEls);
            CORE.triggerEvent({
                type: 'removeAllNewStatus'
            });
            return lastViewedReqTime
        }
    }
    /**
     * Routing storage event handler by event key
     * @param event
     */
    function storageEventRouter(event){
        if(event.key=='lastViewedReqTime'){
            removeAllNewStatus()
        }
    }
    return{
        coreRegister: function(){
            CORE.registerModule(moduleName, this);
            return false
        },
        init: function(){
			var $reqTable;
            that = this;
            reqViewedStatus = false;
            $(function(){
                that.initEditNewStatus();
                if (document.visibilityState == "visible") {
                    that.removeAllNewStatusHandler()
                }
            });
            if (window.addEventListener) {
		        window.addEventListener("focus", that.removeAllNewStatusHandler, false);
		        window.addEventListener("mousemove", that.removeAllNewStatusHandler, false);
                window.addEventListener('storage', storageEventRouter)
	        }
			CORE.registerEvents(moduleName, {
                'newAjaxRespPoll': this.addNewRequests
            });
            return false
        },
		/**
		* Init remove 'NEW' status at requests which are already viewed
		*/
        initEditNewStatus: function(){
            var $trEls,
                lastViewedReq;
            newCount = 0;
            $trEls = cloneDomTrEls();
            if($trEls.length) {
                lastViewedReq = localStorage['lastViewedReqTime'];
                initRemoveNewStatus($trEls, lastViewedReq);
                insertNewReqTable($trEls);
            }
            CORE.triggerEvent({
                type: 'initCountNewStatus',
                data: newCount
            })
        },
        //Facade public method removing all 'NEW' from DOM
        removeAllNewStatusHandler: function(){
            var lastViewedReqTime;
            if(reqViewedStatus==false){
                lastViewedReqTime = removeAllNewStatus(lastViewedReqTime);
                reqViewedStatus = true;
                if(localStorage['lastViewedReqTime']||localStorage['lastViewedReqTime']<lastViewedReqTime){
                    localStorage['lastViewedReqTime'] = lastViewedReqTime
                }
            }
        },
		//Facade ppublic method insrt new tr elements collections to DOM
        addNewRequests: function(data){
            var $trEls;
			$reqTrEls = data.$reqTrEls;
            insertNewReqTable($reqTrEls);
            reqViewedStatus = false
        }
    };
}());
REQTABLE.coreRegister();

AJAXREQ = (function(){
    var that,
        moduleName = 'AJAXREQ',
        ajaxReqPollingInterval,
		newCount;
	//Create data array to mock response from server 
	function getMockAjaxData(){
		var ajaxReqArr,
			reqObj,
			objNum,
            ajaxReqObj,
            arrRandom,
            rand,
            time,
            tmeStr;
        arrRandom = [0, 1, 0];
        rand = Math.floor(Math.random() * arrRandom.length);
        if(rand==0) return {};
        ajaxReqObj = {};
        ajaxReqObj['lastEditTime'] = '2017-04-05T06:33:37';
		ajaxReqArr = [];
        time = new Date();
        timeStr = time.toISOString();
		reqObj = {
			id: 0,
			method: "GET",
			path: "/requests/",
			request_time: timeStr,
			status_code: 200,
            priority: 0
		};
		//objNum = Math.floor(Math.random() * (4));
		for(var i= 1; i < 11; i++){
			ajaxReqArr.push(reqObj)
		}
        ajaxReqObj['ajaxReqArr'] = ajaxReqArr;
		return ajaxReqObj
	}
	//Private helper method take JSON data from server 
	//return tr elements collections to insert in requests table
    function getReqTrEls(ajaxReqArr){
        var reqTrArr,
            $reqTrEls,
            reqTrHtml,
            selectTrEl,
            reqTime,
            reqId,
            reqPrior;
        newCount = 0;
        $reqTrEls = $();
        for (var i=0; i<ajaxReqArr.length; i++) {
            var newVar;
            reqTime = ajaxReqArr[i].request_time;
            if(reqTime>localStorage['lastViewedReqTime']){
                newVar = 'NEW';
                newCount +=1
            }else{
                newVar = ''
            }
            reqId = ajaxReqArr[i].id;
            reqPrior = ajaxReqArr[i].priority;
            selectTrEl = '<select name="'+reqId+'">';
            for (var j=0; j<6; j++){
                if (j==reqPrior){
                    selectTrEl += '<option value="'+j+'" selected>'+j+'</option>';
                }else{
                    selectTrEl += '<option value="'+j+'" >'+j+'</option>';
                }
            }
            selectTrEl += '</select>';
            reqTrArr = [
                +i + 1,
                ajaxReqArr[i].request_time,
                ajaxReqArr[i].path,
                ajaxReqArr[i]['status_code'],
                ajaxReqArr[i]['method'],
                newVar,
                selectTrEl
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
            var $lastEditTime;
            that = this;
            sessionStorage["lastEditTime"] = '';
            $lastEditTime = $('#last_edit_time');
            if ($lastEditTime.length) {
                sessionStorage["lastEditTime"] = $lastEditTime.text();
            }
            that.startGetAjaxReqPolling()
        },
		//Start ajax requests polling via seInterval function
        startGetAjaxReqPolling: function(){
			var ajaxReqObj;
            if(ajaxReqPollingInterval==null){
                ajaxReqPollingInterval = setInterval(function(){
					var ajaxRequestData = {};
					ajaxRequestData['last_edit_time'] = sessionStorage["lastEditTime"];
					//$.get('/requests/', ajaxRequestData).done(that.handleGetAjaxReqPoll)
					ajaxReqObj = getMockAjaxData();
					that.handleGetAjaxReqPoll(ajaxReqObj)
				}, 4000)
            }
        },
		//Handle ajax response data, running helper method and trigger newAjaxRespPoll event
        handleGetAjaxReqPoll: function(ajaxRepObj){
            var $reqTrEls,
                ajaxReqArr,
                lastEditTime;
            if('ajaxReqArr' in ajaxRepObj) {
                lastEditTime = ajaxRepObj.lastEditTime;
                sessionStorage['lastEditTime'] = lastEditTime;
                ajaxReqArr = ajaxRepObj.ajaxReqArr;
				$reqTrEls = getReqTrEls(ajaxReqArr);
				CORE.triggerEvent({
                    type: 'newAjaxRespPoll',
                    data: {
						'$reqTrEls': $reqTrEls,
						'newCount': newCount
					}
                })
            }
            return false
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
	/**
	* Change page title by update newStatus
	*/
    function updatePageTitle(newStatus){
        if(newStatus==0){
            newStatus=''
        }else newStatus='('+newStatus+') ';
        $('title').replaceWith('<title>'+newStatus+'new requests</title>')
    }
    return{
        coreRegister: function() {
            CORE.registerModule(moduleName, this);
        },
        init: function(){
            that = this;
            //newStatus = 0;
            CORE.registerEvents(moduleName,{
                'removeAllNewStatus': this.resetPageHeader,
				'newAjaxRespPoll': this.ajaxUpdatePageHeader,
				'initCountNewStatus': this.initNewStatus
            });
        },
		//Return init count of new requests
		initNewStatus: function(data){
			newStatus = data;
            updatePageTitle(newStatus);
		},
		//Reset page title after removing all 'NEW' status
        resetPageHeader: function(){
            newStatus = 0;
            updatePageTitle(newStatus);
        },
		//Update page title, by new requests 
        ajaxUpdatePageHeader: function(data){
            newStatus += data.newCount;
            if(newStatus > 10){
                newStatus = 10
            }
            updatePageTitle(newStatus);
		}
    };
})();
PAGEHEHEADUPDATE.coreRegister();

CORE.startAllMod()
