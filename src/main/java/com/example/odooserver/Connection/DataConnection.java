package com.example.odooserver.Connection;

import java.util.Map;
import java.lang.Integer;

import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import java.net.URL;

public class DataConnection {

	// ---------------------- Configuration ----------------------

	// final String URL = "localhost:8069";
	// final String DATABASE = "Time_Loop";
	// final String USERNAME = "anaalava@ucm.es";
	// final String PASSWORD = "0d00sg3";

	final String url = "localhost:8069",
              db = "TimeLoop",
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


		// ---------------------- Logging in ----------------------		
		final XmlRpcClientConfigImpl common_config = new XmlRpcClientConfigImpl();
		common_config.setServerURL(
			new URL(String.format("%s/xmlrpc/2/common", url)));
		client.execute(common_config, "version", emptyList());

		int uid = (int)client.execute(
    		common_config, "authenticate", asList(
        		db, username, password, emptyMap()));


		// ---------------------- Calling methods ----------------------
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


		// ---------------------- List records ----------------------
		asList((Object[])models.execute("execute_kw", asList(
			db, uid, password,
			"res.partner", "search",
			asList(asList(
				asList("is_company", "=", true),
				asList("customer", "=", true)))
		)));


		// ---------------------- Pagination ----------------------
		asList((Object[])models.execute("execute_kw", asList(
			db, uid, password,
			"res.partner", "search",
			asList(asList(
				asList("is_company", "=", true),
				asList("customer", "=", true))),
			new HashMap() {{ put("offset", 10); put("limit", 5); }}
		)));


		// ---------------------- Count records ----------------------
		// (Integer)
		models.execute("execute_kw", 
			asList(db, uid, password,
			"res.partner", "search_count",
			asList(asList(
				asList("is_company", "=", true),
				asList("customer", "=", true)))
		));


		// ---------------------- Read records ----------------------
		final List ids = asList((Object[])models.execute(
    		"execute_kw", asList(
        		db, uid, password,
        	"res.partner", "search",
       		asList(asList(
            asList("is_company", "=", true),
            asList("customer", "=", true))),
        		new HashMap() {{ put("limit", 1); }}
			)));

		final Map record = (Map)((Object[])models.execute(
			"execute_kw", asList(
				db, uid, password,
				"res.partner", "read",
				asList(ids)
			)
		))[0];
		// count the number of fields fetched by default
		record.size();


		asList((Object[])models.execute("execute_kw", asList(
			db, uid, password,
			"res.partner", "read",
			asList(ids),
			new HashMap() {{
				put("fields", asList("name", "country_id", "comment"));
			}}
		)));

		// ---------------------- Listing record fields ----------------------
		(Map<String, Map<String, Object>>)models.execute("execute_kw", asList(
    		db, uid, password,
    		"res.partner", "fields_get",
    		emptyList(),
    			new HashMap() {{
        	put("attributes", asList("string", "help", "type"));
    		}}
		));



		// ---------------------- Search and read ----------------------

		asList((Object[])models.execute("execute_kw", asList(
			db, uid, password,
			"res.partner", "search_read",
			asList(asList(
				asList("is_company", "=", true),
				asList("customer", "=", true))),
			new HashMap() {{
				put("fields", asList("name", "country_id", "comment"));
				put("limit", 5);
			}}
		)));


		// ---------------------- Create records ----------------------
		final Integer id = (Integer)models.execute("execute_kw", asList(
			db, uid, password,
			"res.partner", "create",
			asList(new HashMap() {{ put("name", "New Partner"); }})
		));


		
	}
}
