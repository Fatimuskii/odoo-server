package com.example.odooserver.Connection;

import java.util.Map;

import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import java.net.URL;

public class DataConnection {

	// final String URL = "localhost:8069";
	// final String DATABASE = "Time_Loop";
	// final String USERNAME = "anaalava@ucm.es";
	// final String PASSWORD = "0d00sg3";

	final String url = "localhost:8069",
              db = "Time_Loop",
        username = "anaalava@ucm.es",
        password = "0d00sg3";
	
	final XmlRpcClient client = new XmlRpcClient();

	final XmlRpcClientConfigImpl start_config = new XmlRpcClientConfigImpl();
	
	public DataConnection() {
		// start_config.setServerURL(new URL("https://demo.odoo.com/start"));
		start_config.setServerURL(new URL("http://localhost:8069"));
		final Map<String, String> info = (Map<String, String>)client.execute(
		    start_config, "start", emptyList());

		final String url = info.get("host"),
		              db = info.get("database"),
		        username = info.get("user"),
		        password = info.get("password");

		final XmlRpcClientConfigImpl common_config = new XmlRpcClientConfigImpl();
		common_config.setServerURL(
			new URL(String.format("%s/xmlrpc/2/common", url)));
		client.execute(common_config, "version", emptyList());

		int uid = (int)client.execute(
    		common_config, "authenticate", asList(
        		db, username, password, emptyMap()));


		final XmlRpcClient models = new XmlRpcClient() {{
			setConfig(new XmlRpcClientConfigImpl() {{
			setServerURL(new URL(String.format("%s/xmlrpc/2/object", url)));
			}});
		}};
		models.execute("execute_kw", asList(
			db, uid, password,
			"res.partner", "check_access_rights",
			asList("read"),
			new HashMap() {{ put("raise_exception", false); }}
		));


	asList((Object[])models.execute("execute_kw", asList(
		db, uid, password,
		"res.partner", "search",
		asList(asList(
			asList("is_company", "=", true),
			asList("customer", "=", true)))
	)));



	}
}
