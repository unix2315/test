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
	//Private help method, unit new tr element collections with DOM one
    function unitTrEls($trEls, $reqTrEls){
        $trEls = $reqTrEls.add($trEls);
        if($trEls.length > 10){
            $trEls = $trEls.slice(0, 10)
        }
        return $trEls
    }
    //Private help method, removing 'NEW' from td elements
    function removeNewStatus($trEls, lastViewedReq) {
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
            $(function(){
                that.initEditNewStatus()
            });
			//$reqTable = $('#requests_table');
            if (window.addEventListener) {
		        window.addEventListener("focus", that.removeAllNewStatus, false);
		        window.addEventListener("mousemove", that.removeAllNewStatus, false);
	        }
            reqViewedStatus = false;
			CORE.registerEvents(moduleName, {
                'newAjaxRespPoll': this.addNewRequests,
                'tabUpdateTable': this.tabUpdateReqTable
            });
            return false
        },
		/**
		* Insert new table content via addNewRequests/removeAllNewStatus events
		* in active tab
		*/
		tabUpdateReqTable: function(reqTableDomEl){
            var $domReqTable;
            $domReqTable = $('#requests_table_content');
            $domReqTable.replaceWith(reqTableDomEl);
			reqViewedStatus = false;
            return false
        },
		/**
		* Init remove 'NEW' status at requests which are already viewed
		*/
        initEditNewStatus: function(){
            var $trEls,
                lastReqTime,
				newTdEl,
                lastViewedReq;
            newCount = 0;
            $trEls = cloneDomTrEls();
            if($trEls.length) {
                lastReqTime = $trEls[0].getElementsByTagName('td')[1].innerHTML;
                localStorage["lastRequestTime"] = lastReqTime;
                lastViewedReq = localStorage['lastViewedReqTime'];
                removeNewStatus($trEls, lastViewedReq);
                insertNewReqTable($trEls);
            }else{
                localStorage["lastRequestTime"] = ''
            }
            CORE.triggerEvent({
                type: 'initCountNewStatus',
                data: newCount
            })
        },
        //Facade public method removing all 'NEW' from DOM
        removeAllNewStatus: function(){
            var $trEls,
                lastViewedReq,
                reqTableDomEl;
            $trEls = cloneDomTrEls();
            if($trEls.length&&reqViewedStatus==false){
                lastViewedReq = localStorage["lastRequestTime"];
                if(localStorage['lastViewedReqTime']<lastViewedReq){
                    localStorage['lastViewedReqTime'] = lastViewedReq;
                }
                removeNewStatus($trEls, lastViewedReq);
                insertNewReqTable($trEls);
				// Update localStorege to send DOM changes to offline tabs 
                reqTableDomEl = document.getElementById('requests_table_content').outerHTML;
				localStorage.setItem('tabUpdateTable', reqTableDomEl);
                CORE.triggerEvent({
                    type: 'removeAllNewStatus'
                });
                reqViewedStatus = true
            }
        },
		//Facade ppublic method insrt new tr elements collections to DOM
        addNewRequests: function(data){
            var $trEls,
                 reqTableDomEl;
            $trEls = cloneDomTrEls();
			$reqTrEls = data.$reqTrEls;
            if($trEls.length){
                $trEls = unitTrEls($trEls, $reqTrEls)
            }else{
                $trEls = $reqTrEls
            }
            for(var i= 0, max = $trEls.length; i < max; i++){
                updateTabNum(i, $trEls);
            }
            insertNewReqTable($trEls);
			// Update localStorege to send DOM changes to offline tabs
            reqTableDomEl = document.getElementById('requests_table_content').outerHTML;
			localStorage.setItem('tabUpdateTable', reqTableDomEl);
            reqViewedStatus = false;
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
            that = this;
            CORE.registerEvents(moduleName,{
                'startAjaxPolling': this.startGetAjaxReqPolling,
                'stopAjaxPolling': this.stopGetAjaxReqPolling
            });
            this.startGetAjaxReqPolling()
        },
		//Start ajax requests polling via seInterval function
        startGetAjaxReqPolling: function(){
			//var ajaxReqArr;
            if(ajaxReqPollingInterval==null){
                ajaxReqPollingInterval = setInterval(function(){
					var ajaxRequestData = {};
					ajaxRequestData['last_request_time'] = localStorage["lastRequestTime"];
					$.get('/requests/', ajaxRequestData).done(that.handleGetAjaxReqPoll)
					//ajaxReqArr = getMockAjaxData();
					//that.handleGetAjaxReqPoll(ajaxReqArr)
				}, 4000)
            }
        },
		//Handle ajax response data, running helper method and trigger newAjaxRespPoll event
        handleGetAjaxReqPoll: function(ajaxReqArr){
            var $reqTrEls;
            if(ajaxReqArr.length) {
                localStorage["lastRequestTime"] = ajaxReqArr[0].request_time;
				$reqTrEls = getReqTrEls(ajaxReqArr);
				CORE.triggerEvent({
                    type: 'newAjaxRespPoll',
                    data: {
						'$reqTrEls': $reqTrEls,
						'newCount': newCount
					}
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
				'initCountNewStatus': this.initNewStatus,
                'tabUpdateTitle': updatePageTitle
            });
        },
		//Return init count of new requests
		initNewStatus: function(data){
			newStatus = data;
            updatePageTitle(newStatus);
            //localStorage.setItem('tabUpdateTitle', newStatus)
		},
		//Reset page title after removing all 'NEW' status
        resetPageHeader: function(){
            newStatus = 0;
            updatePageTitle(newStatus);
            localStorage.setItem('tabUpdateTitle', newStatus)
        },
		//Update page title, by new requests 
        ajaxUpdatePageHeader: function(data){
            newStatus += data.newCount;
            if(newStatus > 10){
                newStatus = 10
            }
            updatePageTitle(newStatus);
            localStorage.setItem('tabUpdateTitle', newStatus)
		}
    };
})();
PAGEHEHEADUPDATE.coreRegister();

TABSINTERACTIONS = (function(){
    var moduleName,
		tabId,
        that;
    moduleName = 'TABSINTERACTIONS';
    /**
     * Helper method to get unique ID for new tab
     * @returns {string}
     */
    function getUniqueId(){
        return '_' + Math.random().toString(36).substr(2, 9);
    }
    /**
     * Modify openTabs obj, remove closed tabs, and set one as active
     */
    function removeTabId(){
        var openTabs,
            onlineTab;
        openTabs = JSON.parse(localStorage['openTabs']);
        delete openTabs[tabId];
        for (var tab in openTabs) {
            if (openTabs.hasOwnProperty(tab)) {
                if(openTabs[tab]=='active') {
                    onlineTab=undefined;
                    break
                } else {
                    onlineTab = tab
                }
            }
        }
        if (onlineTab!=undefined) {
            openTabs[onlineTab] = 'active'
        }
        localStorage.setItem('openTabs', JSON.stringify(openTabs));
    }
    /**
     * Modify openTabs obj, add active tab and reset others
     * Trigger startPolling event if tab is active
     */
    function handleWinFocus(){
        var openTabs;
        CORE.triggerEvent({
            type: 'startAjaxPolling'
        });
        openTabs = JSON.parse(localStorage['openTabs']);
        if(openTabs[tabId]!='active'){
            for(var tab in openTabs){
                if (openTabs.hasOwnProperty(tab)) {
                    if(tab==tabId){
                        openTabs[tab] = 'active';
                    }else{
                        openTabs[tab] = 'offline';
                    }
                }
            }
        }
        localStorage.setItem('openTabs', JSON.stringify(openTabs));
    }
    /**
     * Start/stop ajax polling by update tab status via storage event
     */
    function manageAjaxPolling(){
        var openTabs;
        openTabs = JSON.parse(localStorage['openTabs']);
        if(openTabs[tabId]=='active'){
            CORE.triggerEvent({
                type: 'startAjaxPolling'
            });
        }else if(openTabs[tabId]=='offline'){
            CORE.triggerEvent({
                type: 'stopAjaxPolling'
            });
        }
    }

    /**
     * Routing storage event handler by event key
     * @param event
     */
    function storageEventRouter(event){
        var reqTableDomEl,
            newStatus;
        if(event.key=='openTabs'){
            manageAjaxPolling()
        }else if(event.key=='tabUpdateTable'){
            reqTableDomEl = localStorage['tabUpdateTable'];
            CORE.triggerEvent({
                type: 'tabUpdateTable',
                data: reqTableDomEl
            });
        }else if(event.key=='tabUpdateTitle'){
            newStatus = localStorage['tabUpdateTitle'];
            CORE.triggerEvent({
                type: 'tabUpdateTitle',
                data: newStatus
            });
        }
    }
    return{
        coreRegister: function() {
            CORE.registerModule(moduleName, this);
        },
        init: function() {
            var openTabs;
            that = this;
            tabId = getUniqueId();
            $(function () {
                if(localStorage['openTabs']){
                    openTabs = JSON.parse(localStorage['openTabs']);
                    for(var tab in openTabs) {
                        if (openTabs.hasOwnProperty(tab)) {
                            if (openTabs[tab]=='active') {
                                openTabs[tabId] = 'offline';
                                break
                            }else openTabs[tabId] = 'active'
                        }
                    }
                    if(!openTabs[tabId]){
                        openTabs[tabId] = 'active'
                    }
                }else{
                    openTabs = {};
                    openTabs[tabId] = 'active'
                }
                localStorage.setItem('openTabs', JSON.stringify(openTabs))
            });
            window.addEventListener('focus', handleWinFocus);
            window.addEventListener('mousemove', handleWinFocus);
            window.addEventListener('unload', removeTabId);
            window.addEventListener('storage', storageEventRouter)
        }
    };
})();
TABSINTERACTIONS.coreRegister();

CORE.startAllMod()
