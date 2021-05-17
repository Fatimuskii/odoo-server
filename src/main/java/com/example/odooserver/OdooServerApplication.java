package com.example.odooserver;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class OdooServerApplication {

	public static void main(String[] args) {
		SpringApplication.run(OdooServerApplication.class, args);

		try {
			XmlRpcClient client = new XmlRpcClient();
			XmlRpcClientConfigImpl clientConfig = new XmlRpcClientConfigImpl();
			clientConfig.setEnabledForExtensions(true);
			clientConfig.setServerURL(new URL("http", "localhost", 8069,
					"/xmlrpc/object"));
			client.setConfig(clientConfig);
			// Vector<Object> arg = new Vector<Object>();
			// arg.add("TimeLoop");             // DB name
			// arg.add(1);                    // used_id
			// arg.add("0d00sg3");          // DB password
			// arg.add("res.partner");        // table 
			// arg.add("read");
			// arg.add(5);                    // Table id 
			// arg.add("name");               // column name 
			// HashMap<Object, Object> ids = new HashMap<Object, Object>();
			// ids = (HashMap<Object, Object>) client.execute("execute", arg);
			// System.out.println(ids);
			// System.out.println(ids.size());

			HashMap<Object, Object> ids =  asList((Object[])models.execute("execute_kw", asList(
				"TimeLoop", 1, "0d00sg3",
				"res.partner", "search_read",
				asList(asList(
					asList("is_company", "=", true),
					asList("customer", "=", true))),
				new HashMap() {{
					put("fields", asList("name", "country_id", "comment"));
					put("limit", 5);
				}}
			)));

			System.out.println(ids);
		}
		catch (Exception e) {
			System.out.println(e.getMessage());
		}
		
	}

}
