class JsCommind(object):
    func_str = """
            function onCallback (response){
                //结果集
                GTSEvent.event(DataEvent.ACCEPTDATA,response);
            }
            """

    def singel_stock_js(self, stocks: str, fields="Code,Name,SectorID,SectorName,MarginTrade,StockConnect"):
        cmd = self.func_str + """
            let stockInformation = NSDK.createRequestItem(SDK_REQUEST_NSTOCKINFO);
            stockInformation.setDataCallback(onCallback);""" + f"""
            stockInformation.setCodes("{stocks}");
            stockInformation.setFields("{fields}");
            stockInformation.request();
        """
        return cmd

    def snapshotUpdowns_js(self, stock_code):
        snap_cmd = self.func_str + """
        let snapshotUpdowns = NSDK.createRequestItem(SDK_REQUEST_UPDOWNDISTRIBUTION);
        //设置回调函数
        snapshotUpdowns.setDataCallback(onCallback);""" + f"""
        snapshotUpdowns.setCode("{stock_code}");
        //开始查询
        snapshotUpdowns.request();
        """
        return snap_cmd

    def kLine_js(self, stock_code="600000.SH", startDay="20201124", endDay="20210315", fields="$all",
                 isSubcrible="true",
                 size=10):
        kline_cmd = self.func_str + """
            let kLine = NSDK.createRequestItem(SDK_REQUEST_KLINE);
            kLine.setDataCallback(onCallback);
        """ + f"""
            kLine.setCode("{stock_code}");
            kLine.setPeriod(SDK_KLINE_PERIOD_DAY);
            kLine.setCqMode(SDK_KLINE_CQMODE_FORWARD);
            kLine.setLimit(-1,{size});
            kLine.setDateRange("{startDay}","{endDay}");
            kLine.setFields("{fields}");
            kLine.setSubscribe({isSubcrible});
            //开始查询
            kLine.request();
        """
        return kline_cmd

    def order_js(self, stock_code="000001.SZ", limit=10, fields="all", isSubcrible=True):
        order_cmd = self.func_str + """
            let order  = NSDK.createRequestItem(SDK_REQUEST_ORDER);
            //设置回调函数
            order.setDataCallback(onCallback);
        """ + f"""
            order.setCode("{stock_code}");
            order.setLimit(-1,{limit});
            order.setFields("${fields}");
            order.setSubscribe({isSubcrible});
            //开始查询
            order.request();
        """
        return order_cmd

    def step_order_js(self, stock_code='000001.SZ', limit=10, fields="all", isSubcrible=True):
        step_cmd = self.func_str + """
            let step  = NSDK.createRequestItem(SDK_REQUEST_STEP);
            //设置回调函数
            step.setDataCallback(onCallback);
        """ + f"""
            step.setCode("{stock_code}");
            step.setWithdrawal(false);
            step.setLimit(-1,{limit});
            step.setFields("${fields}");
            step.setSubscribe({isSubcrible});
            //开始查询
            step.request();
        """
        return step_cmd

    def ticket_js(self, stock_code='000001.SZ', limit=10, fields="all", isSubcrible=True):
        step_cmd = self.func_str + """
            let tick  = NSDK.createRequestItem(SDK_REQUEST_TICK);
            //设置回调函数
            tick.setDataCallback(onCallback);""" + f"""
            tick.setCode("{stock_code}");
            tick.setLimit(-1,{limit});
            tick.setFields("${fields}");
            tick.setSubscribe({isSubcrible});
            //开始查询
            tick.request();
        """
        return step_cmd

    def sort_js(self, stock_code='000001.SZ,600000.SH,688588.SH', limit=10, sortedFields="PercentChange"):
        sort_cmd = self.func_str + """
            let sort = NSDK.createRequestItem(SDK_REQUEST_SORT);
            //设置回调函数
            sort.setDataCallback(onCallback);""" + f"""
            sort.setCodes("{stock_code}");
            sort.setSectorId("101010199911000");
            sort.setSortField("{sortedFields}",SDK_SORTTYPE_DESC);
            sort.setLimit(-1,{limit});
            //开始查询
            sort.request();
        """
        return sort_cmd

    def trend_js(self, stock_code='000001.SZ', days=1, fields="all", subcrible=True):
        trend_cmd = self.func_str + f"""
            let trend  = NSDK.createRequestItem(SDK_REQUEST_TREND);
            //设置回调函数
            trend.setDataCallback(onCallback);
            trend.setCode("{stock_code}");
            trend.setDays({days});
            trend.setFields("${fields}");
            trend.setSubscribe({subcrible});
            //开始查询
            trend.request();
        """
        return trend_cmd

    def hisTrend_js(self, stock_code='000001.SZ', date="20210524", fields="all"):
        hisTrend_cmd = self.func_str + f"""
            let hisTrend  = NSDK.createRequestItem(SDK_REQUEST_HISTREND);
            //设置回调函数
            hisTrend.setDataCallback(onCallback);
            hisTrend.setCode("{stock_code}");
            hisTrend.setDate("{date}");
            hisTrend.setFields("${fields}");
            //开始查询
            hisTrend.request();
        """
        return hisTrend_cmd

    def callAution_js(self, stock_code='000001.SZ', fields="all", subcrible=True):
        callAution_cmd = self.func_str + f"""
            let callAution  = NSDK.createRequestItem(SDK_REQUEST_CALLAUTION);
            //设置回调函数
            callAution.setDataCallback(onCallback);
            callAution.setCode("{stock_code}");
            callAution.setFields("${fields}");
            callAution.setSubscribe({subcrible});
            //开始查询
            callAution.request();
        """
        return callAution_cmd

    def subscribe_js(self, stock_code='000001.SZ,000002.SZ', fields="code,last,change"):
        subscribe_cmd = self.func_str + f"""
            let subscribe   = NSDK.createRequestItem(SDK_REQUEST_QUOTESUBSCRIBE);
            //设置回调函数
            subscribe.setDataCallback(onCallback);
            subscribe.setCodes("{stock_code}");
            subscribe.setFields("{fields}");
            //开始查询
            subscribe.request();
        """
        return subscribe_cmd

    def price_js(self, stock_code='000001.SZ,000002.SZ', limit=10, fields="all", subcrible=True):
        price_cmd = self.func_str + f"""
            let price   = NSDK.createRequestItem(SDK_REQUEST_PRICEDISTRIBUTION);
            //设置回调函数
            price.setDataCallback(onCallback);
            price.setCode("{stock_code}");
            price.setLimit(-1,{limit});
            price.setFields("${fields}");
            price.setSubscribe({subcrible});
            //开始查询
            price.request();
        """
        return price_cmd

    def select_plate_js(self):
        sel_plate_cmd = self.func_str + """
            let requestCommon = NSDK.createRequestItem(SDK_REQUEST_REQUESTCOMMON);
            //设置回调函数
            requestCommon.setDataCallback(onCallback);
            requestCommon.setAPI(SDK_USERSECTOR_GET);
            requestCommon.setParam(SDK_USERSECTOR_USERID,"{{ userid }}");""" + f"""
            requestCommon.setParam(SDK_USERSECTOR_FIELDS,SDK_USERSECTOR_FIELDS_VALUE);
            //开始查询
            requestCommon.request();
        """
        return sel_plate_cmd

    def add_plate_js(self, plate_name):
        add_plate_cmd = self.func_str + """
            let requestCommon = NSDK.createRequestItem(SDK_REQUEST_REQUESTCOMMON);
            //设置回调函数
            requestCommon.setDataCallback(onCallback);
            requestCommon.setAPI(SDK_USERSECTOR_ADD);
            requestCommon.setParam(SDK_USERSECTOR_FIELDS,"sectorid");
            requestCommon.setParam(SDK_USERSECTOR_USERID, "{{ userid }}");""" + f"""
            requestCommon.setParam(SDK_USERSECTOR_SECTORNAME,'{plate_name}');//添加的板块名称
            //开始查询
            requestCommon.request();
        """
        return add_plate_cmd

    def del_plate_js(self, plate_id='1537874208340045824'):
        del_plate_cmd = self.func_str + """
            let requestCommon = NSDK.createRequestItem(SDK_REQUEST_REQUESTCOMMON);
            //设置回调函数
            requestCommon.setDataCallback(onCallback);
            requestCommon.setAPI(SDK_USERSECTOR_DELETE);
            requestCommon.setParam(SDK_USERSECTOR_USERID, "{{ userid }}");""" + f"""
            requestCommon.setParam(SDK_USERSECTOR_SECTORID, "{plate_id}");//删除的板块id
            //开始查询
            requestCommon.request();
        """
        return del_plate_cmd

    def rename_plate_js(self, new_name, plate_id='1537874208340045824'):
        rename_plate_cmd = self.func_str + """
            let requestCommon = NSDK.createRequestItem(SDK_REQUEST_REQUESTCOMMON);
            //设置回调函数
            requestCommon.setDataCallback(onCallback);
            requestCommon.setAPI(SDK_USERSECTOR_EDIT);
            requestCommon.setParam(SDK_USERSECTOR_USERID, "{{ userid }}");""" + f"""
            requestCommon.setParam(SDK_USERSECTOR_SECTORID, "{plate_id}");//板块id
            requestCommon.setParam(SDK_USERSECTOR_SECTORNAME, '{new_name}');
            //开始查询
            requestCommon.request();
        """
        return rename_plate_cmd

    def move_plate_js(self, index=0, plate_id='1537874208340045824'):
        move_plate_cmd = self.func_str + """
            let requestCommon = NSDK.createRequestItem(SDK_REQUEST_REQUESTCOMMON);
            //设置回调函数
            requestCommon.setDataCallback(onCallback);
            requestCommon.setAPI(SDK_USERSECTOR_MOVE);
            requestCommon.setParam(SDK_USERSECTOR_USERID, "{{ userid }}");""" + f"""
            requestCommon.setParam(SDK_USERSECTOR_SECTORID, "{plate_id}");//移动的板块
            requestCommon.setParam(SDK_USERSECTOR_TARGETINDEX, {index});//移动到的下标 0开始
            //开始查询
            requestCommon.request();
        """
        return move_plate_cmd

    def search_mystock_js(self, plate_id='1537874208340045824', fields='secucode'):
        search_mystock_cmd = self.func_str + """
            let requestCommon = NSDK.createRequestItem(SDK_REQUEST_REQUESTCOMMON);
            //设置回调函数
            requestCommon.setDataCallback(onCallback);
            requestCommon.setAPI(SDK_USERSECURITY_GET);
            requestCommon.setParam(SDK_USERSECURITY_USERID,"{{ userid }}");""" + f"""
            requestCommon.setParam(SDK_USERSECURITY_SECTORID,"{plate_id}");//被查询板块的id
            requestCommon.setParam("fields","{fields}");//查询字段
            //开始查询
            requestCommon.request();
        """
        return search_mystock_cmd

    def add_mystock_js(self, plate_id='1537874208340045824', stock='600000.SH'):
        add_mystock_cmd = self.func_str + """
            let requestCommon = NSDK.createRequestItem(SDK_REQUEST_REQUESTCOMMON);
            requestCommon.setDataCallback(onCallback);
            //设置回调函数
            requestCommon.setAPI(SDK_USERSECURITY_ADD);
            requestCommon.setParam(SDK_USERSECURITY_USERID, "{{ userid }}");""" + f"""
            requestCommon.setParam(SDK_USERSECURITY_SECTORID, "{plate_id}");//添加股票的板块id
            requestCommon.setParam(SDK_USERSECURITY_SECURITYS, "{stock}");//添加的股票代码
            //开始查询
            requestCommon.request();
        """
        return add_mystock_cmd
