package com.example.odooserver.Connection;

import java.util.Map;

import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import java.net.URL;

public class DataConnection {

	final String URL = "localhost:8069";
	final String DATABASE = "Time-Loop";
	final String USERNAME = "admin";
	final String PASSWORD = "admin";
	
	final XmlRpcClient client = new XmlRpcClient();

	final XmlRpcClientConfigImpl start_config = new XmlRpcClientConfigImpl();
	
	public DataConnection() {
		start_config.setServerURL(new URL("https://demo.odoo.com/start"));
		final Map<String, String> info = (Map<String, String>)client.execute(
		    start_config, "start", emptyList());

		final String url = info.get("host"),
		              db = info.get("database"),
		        username = info.get("user"),
		        password = info.get("password");
	}


}
